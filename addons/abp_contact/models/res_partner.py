from odoo import fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"
    
    is_customer = fields.Boolean(string='Is customer?', default=0)
    is_vendor = fields.Boolean(string='Is vendor?', default=0)
    
    # Override write instead of onchange because somehow onchange doesn't work
    def write(self, vals):
        if 'is_customer' in vals:
            if vals.get('is_customer') == True:
                vals['customer_rank'] = 1
            else:
                vals['customer_rank'] = 0
                
        if 'is_vendor' in vals:
            if vals.get('is_vendor') == True:
                vals['supplier_rank'] = 1
            else:
                vals['supplier_rank'] = 0
                
        return super().write(vals)
    