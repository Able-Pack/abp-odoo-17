# Face Attendance Scan Logs

Companion addon for hr_attendance_face_detection (Odoo 17).
Attendance > Face Attendance Scan Logs provides read-only history and standard Odoo export.
Administrators see logs in allowed companies; attendance officers see their own scans and managed employees.

Records every request to /face_recognition/check, including failed recognition and geofencing.
On the vendor Face Attendance page, it also records camera/liveness failures and cancellations.
A started scan without a final browser/server response remains "Started / No final result".
Offline attempts that never reach the server cannot be guaranteed to be recorded.
Scan images and biometric encodings are not stored in logs. Browser failure messages are client-reported.
Successful attendance links are captured from actual server-side create/write operations.
Logs cannot be edited/deleted by attendance users. No automatic retention/deletion is configured.
