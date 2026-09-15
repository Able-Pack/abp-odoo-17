// Companion hooks for the vendor's classic frontend script.
(function () {
    if (typeof startFaceRecognition !== "function") return;
    const originalFetch = window.fetch.bind(window);
    let active = null;

    async function logRpc(route, params) {
        const response = await originalFetch(route, {
            method: "POST", headers: {"Content-Type": "application/json"},
            body: JSON.stringify({jsonrpc: "2.0", method: "call", params}),
            keepalive: true,
        });
        const data = await response.json();
        if (!response.ok || data.error) throw new Error("Scan log could not be saved");
        return data.result;
    }
    function finish(attempt, state, message) {
        if (!attempt || attempt.finished) return;
        attempt.finished = true;
        attempt.id.then(id => logRpc("/face_recognition/log/finish", {
            scan_log_id: id, state, message: String(message).slice(0, 2000),
        })).catch(error => console.warn("Face scan log:", error));
    }
    const originalStart = startFaceRecognition;
    startFaceRecognition = function () {
        if (isProcessing || event.target.disabled) return;
        active = {finished: false, id: logRpc("/face_recognition/log/start", {}).then(r => r.id)};
        active.id.catch(error => console.warn("Face scan log:", error));
        return originalStart.apply(this, arguments);
    };
    window.fetch = async function (url, options) {
        if (url === "/face_recognition/check" && active && options && options.body) {
            const attempt = active;
            const payload = JSON.parse(options.body);
            try {
                payload.params.scan_log_id = await attempt.id;
            } catch (error) {
                // The server creates a log itself if the start request failed.
            }
            return originalFetch(url, {...options, body: JSON.stringify(payload)});
        }
        return originalFetch(url, options);
    };
    const originalNotify = showNotification;
    showNotification = function (type, title, message) {
        if (type === "error") {
            const text = document.createElement("div");
            text.innerHTML = String(message);
            finish(active, "failed", text.textContent);
        }
        return originalNotify.apply(this, arguments);
    };
    const originalCleanup = cleanupCamera;
    cleanupCamera = function () {
        const status = document.getElementById("liveness-status");
        const failed = status && status.classList.contains("alert-danger");
        finish(active, failed ? "failed" : "cancelled",
            failed ? status.textContent : "Camera closed or scan cancelled.");
        active = null;
        return originalCleanup.apply(this, arguments);
    };
})();
