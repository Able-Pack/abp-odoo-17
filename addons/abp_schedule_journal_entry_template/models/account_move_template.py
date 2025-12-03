# -*- coding: utf-8 -*-
import pytz
from datetime import datetime
from odoo import models, fields


class AccountMoveTemplate(models.Model):
    _inherit = 'account.move.template'

    post_schedule_date = fields.Integer(string='Post Schedule Date', help='The day of the month when the journal entry is scheduled to be posted.')

    def post_scheduled_entry_template(self):
        """Posts journal entries based on the schedule date."""

        # Get timezone from first available user or default to UTC
        user = self.env['res.users'].sudo().search([], limit=1)
        user_tz = user.tz if user and user.tz else None
        user_pytz = pytz.timezone(user_tz) if user_tz else pytz.utc
        now_dt = datetime.now().astimezone(user_pytz).replace(tzinfo=None)
        
        for template in self.search([('post_schedule_date', '!=', False)]):
            template_post_schedule_date = template.post_schedule_date
            if template_post_schedule_date == now_dt.day:
                template.generate_journal_entry()