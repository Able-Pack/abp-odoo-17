# Face Attendance Scan Logs

Integrated into hr_attendance_face_detection (Odoo 17). Upgrade this module to enable scan logs, Google Maps links and embedded maps. The standard Kiosk Mode menu is temporarily hidden.
Attendance > Face Attendance Scan Logs provides read-only history and standard Odoo export.
Administrators see logs in allowed companies; attendance officers see their own scans and managed employees.

Records every request to /face_recognition/check, including failed recognition and geofencing.
On the vendor Face Attendance page, it also records camera/liveness failures and cancellations.
A started scan without a final browser/server response remains "Started / No final result".
Offline attempts that never reach the server cannot be guaranteed to be recorded.
Scan images and biometric encodings are not stored in logs. Browser failure messages are client-reported.
Successful attendance links are captured from actual server-side create/write operations.
Logs cannot be edited/deleted by attendance users. No automatic retention/deletion is configured.

Location matching stores the nearest same-company location within its radius using Haversine distance in meters. Location, Location Status, and Distance (m) are available in list/form/export. Overlapping equal-distance locations use the lowest ID. No match is Outside configured locations; missing/invalid GPS is No GPS. Names and distances survive location edits/deletion. Version 17.0.0.4 backfills existing logs using current settings once; historical settings cannot be reconstructed.

Location configuration accepts Google Maps links. Paste a full link with coordinates or a Google Maps short link; coordinates are populated on change and validated on save. Place-pin coordinates take priority over map-view coordinates. Short links require outbound HTTPS to the allowed Google Maps hosts; no page scripts are executed. If expansion fails, paste the expanded URL or enter coordinates manually. Radius remains a manual meter value.

Able Pack attendance menus are controlled by abp_security: Administrator sees active attendance menus; Supervisor and Salesperson see only Face Attendance. Configuration provides Face Attendance Locations; general Settings retains the existing system-administrator requirement. Kiosk remains hidden. Menu filtering does not revoke existing model ACLs or direct API access. Upgrade both modules for these changes.
