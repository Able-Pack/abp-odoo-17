from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"
    
    is_customer = fields.Boolean(string='Is customer?', default=0, compute='_compute_rank', inverse='_set_is_customer')
    is_vendor = fields.Boolean(string='Is vendor?', default=0, compute='_compute_rank', inverse='_set_is_vendor')
    
    # Override write instead of onchange because somehow onchange doesn't work
    # def write(self, vals):
    #     if 'is_customer' in vals:
    #         vals['customer_rank'] = vals.get('is_customer')
                
    #     if 'is_vendor' in vals:
    #         vals['supplier_rank'] = vals.get('is_vendor')
                
    #     return super().write(vals)
    
    def _set_is_customer(self):
        self.customer_rank = self.is_customer
        
    def _set_is_vendor(self):
        self.supplier_rank = self.is_vendor
    
    @api.depends('customer_rank', 'supplier_rank')
    def _compute_rank(self):
        for rec in self:
            rec.is_customer = rec.customer_rank
            rec.is_vendor = rec.supplier_rank
    