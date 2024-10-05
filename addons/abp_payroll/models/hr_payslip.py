from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    date_created = fields.Date(string="Date Created", required=True, default=fields.Date.context_today)
    