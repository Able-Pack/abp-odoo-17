def migrate(cr, version):
    # Transfer ownership before loading XML to preserve records and model metadata.
    cr.execute("""
        UPDATE ir_model_data
           SET module = 'hr_attendance_face_detection'
         WHERE module = 'hr_attendance_face_detection_log'
           AND NOT EXISTS (
               SELECT 1 FROM ir_model_data target
                WHERE target.module = 'hr_attendance_face_detection'
                  AND target.name = ir_model_data.name
           )
    """)