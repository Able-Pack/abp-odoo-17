from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"
    
    role_type = fields.Selection(string='Type',
        selection=[('customer', 'Customer'), ('vendor', 'Vendor')],
    )
    
    customer_catalogue_ids = fields.One2many(comodel_name='customer.catalogue', inverse_name='partner_id')
    
    @api.onchange('role_type')
    def onchange_role_type(self):
        for rec in self:
            if rec.role_type == 'customer':
                rec.customer_rank = 1
                rec.supplier_rank = 0
            elif rec.role_type == 'vendor':
                rec.customer_rank = 0
                rec.supplier_rank = 1
                