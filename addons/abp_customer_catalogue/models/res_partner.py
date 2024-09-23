from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"
    
    customer_catalogue_ids = fields.One2many(comodel_name='customer.catalogue', inverse_name='partner_id')
    