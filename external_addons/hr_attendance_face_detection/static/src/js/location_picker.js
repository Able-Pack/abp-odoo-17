/** @odoo-module **/
import { Component, xml, useRef, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS, loadCSS } from "@web/core/assets";
import { Dialog } from "@web/core/dialog/dialog";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class LocationDialog extends Component {
    static components = { Dialog };
    static props = ["close", "record"];
    static template = xml`
        <Dialog title="'Select Attendance Location'" size="'lg'">
            <p>Click the map or drag the pin. The circle shows the attendance radius.</p>
            <div t-if="state.error" class="alert alert-warning" t-esc="state.error"/>
            <div t-if="!state.ready and !state.error">Loading map...</div>
            <div t-ref="map" style="height:400px;width:100%"/>
            <div class="mt-3 d-flex flex-wrap gap-3 align-items-center">
                <span>Latitude: <t t-esc="state.lat.toFixed(7)"/></span>
                <span>Longitude: <t t-esc="state.lng.toFixed(7)"/></span>
                <label>Radius (meters) <input aria-label="Radius (meters)" type="number" min="0" step="any" class="form-control" t-att-value="state.radius" t-on-input="radiusChanged"/></label>
            </div>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-att-disabled="!state.ready || state.saving || !state.validRadius" t-on-click="apply">Use This Location</button>
                <button class="btn btn-secondary" t-on-click="props.close">Cancel</button>
            </t>
        </Dialog>`;
    setup() {
        this.mapRef = useRef("map");
        const data = this.props.record.data;
        this.state = useState({lat: data.face_attendance_latitude || 0,
            lng: data.face_attendance_longitude || 0,
            radius: Math.max(0, data.face_attendance_radius || 0), validRadius: true,
            ready: false, saving: false, error: ""});
        onMounted(() => this.initMap());
        onWillUnmount(() => { this.disposed = true; if (this.map) this.map.remove(); });
    }
    async initMap() {
        try {
            // Same Leaflet and OpenStreetMap providers used by the vendor attendance page.
            await Promise.all([loadJS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
                loadCSS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")]);
            if (this.disposed) return;
            const L = window.L;
            const point = [this.state.lat, this.state.lng];
            this.map = L.map(this.mapRef.el).setView(point, this.state.lat || this.state.lng ? 16 : 2);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).on("tileerror", () => {
                if (!this.disposed) this.state.error = "Some map tiles could not load. Check your internet connection.";
            }).addTo(this.map);
            this.marker = L.marker(point, {draggable: true}).addTo(this.map);
            this.circle = L.circle(point, {radius: this.state.radius}).addTo(this.map);
            this.map.on("click", (event) => this.select(event.latlng));
            this.marker.on("dragend", () => this.select(this.marker.getLatLng()));
            this.state.ready = true;
            this.map.invalidateSize();
        } catch (error) {
            if (!this.disposed) this.state.error = "Map could not load. Close this dialog and paste a Google Maps link or enter coordinates manually.";
        }
    }
    select(point) {
        this.state.lat = Number(Math.max(-90, Math.min(90, point.lat)).toFixed(7));
        this.state.lng = Number((((point.lng + 180) % 360 + 360) % 360 - 180).toFixed(7));
        const coords = [this.state.lat, this.state.lng];
        this.marker.setLatLng(coords);
        this.circle.setLatLng(coords);
    }
    radiusChanged(event) {
        const value = Number(event.target.value);
        this.state.validRadius = event.target.value !== "" && Number.isFinite(value) && value >= 0;
        if (this.state.validRadius) {
            this.state.radius = value;
            if (this.circle) this.circle.setRadius(value);
        }
    }
    async apply() {
        this.state.saving = true;
        try {
            // Keep the link in sync so the server does not restore an older pin on save.
            await this.props.record.update({face_attendance_latitude: this.state.lat,
                face_attendance_longitude: this.state.lng, face_attendance_radius: this.state.radius,
                google_maps_link: `https://www.google.com/maps?q=${this.state.lat.toFixed(7)},${this.state.lng.toFixed(7)}`});
            this.props.close();
        } finally { this.state.saving = false; }
    }
}
class LocationPicker extends Component {
    static props = {...standardFieldProps};
    static template = xml`<button type="button" class="btn btn-link p-0" t-att-disabled="props.readonly" t-on-click.stop="open">Select on Map</button>`;
    setup() { this.dialog = useService("dialog"); }
    open() { this.dialog.add(LocationDialog, {record: this.props.record}); }
}
registry.category("fields").add("attendance_location_picker", {component: LocationPicker, supportedTypes: ["boolean"]});