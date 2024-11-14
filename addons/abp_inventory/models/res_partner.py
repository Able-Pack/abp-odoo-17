from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    location_src_id = fields.Many2one(comodel_name='stock.location', string='Source Location')
    location_dest_id = fields.Many2one(comodel_name='stock.location', string='Destination Location')