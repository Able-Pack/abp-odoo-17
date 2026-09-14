{
    "name": "Face Attendance Scan Logs",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["hr_attendance_face_detection"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/scan_log_views.xml",
    ],
    "assets": {"web.assets_frontend": [
        ("after", "hr_attendance_face_detection/static/src/js/face_page.js",
         "hr_attendance_face_detection_log/static/src/js/scan_log.js")
    ]},
    "installable": True,
}
