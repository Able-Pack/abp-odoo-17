from unittest.mock import patch, MagicMock
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestMapsLink(TransactionCase):
    def test_coordinate_formats_and_persistence(self):
        model = self.env['multi.location']
        for url in [
            'https://www.google.com/maps?q=1.3528,103.8205',
            'https://www.google.com/maps/search/?api=1&query=1.3528%2C103.8205',
            'https://www.google.com/maps/@1.3528,103.8205,17z',
            'https://www.google.com/maps/place/Test/@1,2,17z/data=!3d1.3528!4d103.8205',
        ]:
            values = model._coordinates_from_maps_link(url)
            self.assertEqual(values['face_attendance_latitude'], 1.3528)
            self.assertEqual(values['face_attendance_longitude'], 103.8205)
        location = model.create({'name': 'QA link', 'google_maps_link': url})
        self.assertEqual(location.face_attendance_latitude, 1.3528)
        location.write({'google_maps_link': 'https://maps.google.com/?q=0,0'})
        self.assertEqual(location.face_attendance_latitude, 0)
        self.assertEqual(location.face_attendance_longitude, 0)
        draft = model.new({'google_maps_link': url})
        draft._onchange_google_maps_link()
        self.assertEqual(draft.face_attendance_longitude, 103.8205)

    def test_invalid_links_and_short_redirects(self):
        model = self.env['multi.location']
        for url in ['https://evil.example/maps?q=1,2', 'http://google.com/maps?q=1,2',
                    'https://google.com/maps?q=91,2', 'https://google.com/maps?q=Singapore',
                    'https://google.com.evil.example/maps?q=1,2']:
            with self.assertRaises(ValidationError):
                model._coordinates_from_maps_link(url)
        with patch('odoo.addons.hr_attendance_face_detection.models.multi_location.requests.Session') as session:
            response = MagicMock(status_code=302)
            response.headers = {'Location': 'https://www.google.com/maps?q=1.3528,103.8205'}
            session.return_value.__enter__.return_value.get.return_value.__enter__.return_value = response
            self.assertEqual(model._coordinates_from_maps_link('https://maps.app.goo.gl/test')['face_attendance_latitude'], 1.3528)
            response.headers = {'Location': 'https://127.0.0.1/private'}
            with self.assertRaises(ValidationError):
                model._coordinates_from_maps_link('https://maps.app.goo.gl/test')