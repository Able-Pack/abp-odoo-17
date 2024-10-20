from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"
    
    # Redefine fields because somehow these fields cannot be used for api.depends
    supplier_rank = fields.Integer(default=0, copy=False)
    customer_rank = fields.Integer(default=0, copy=False)
    
    is_customer = fields.Boolean(string='Is customer?', default=0, compute='_compute_rank', inverse='_set_is_customer')
    is_vendor = fields.Boolean(string='Is vendor?', default=0, compute='_compute_rank', inverse='_set_is_vendor')
    
    # Override name search method to let user search contacts by street, street2, and zip
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        if not (name == '' and operator in ('like', 'ilike')):
            if domain is None:
                domain = []
            domain += [
                '|', '|', '|',
                ('street', operator, name),
                ('street2', operator, name),
                ('zip', operator, name)
            ]
        return super()._name_search(name, domain, operator, 100, order)
    
    def _set_is_customer(self):
        self.customer_rank = self.is_customer
        
    def _set_is_vendor(self):
        self.supplier_rank = self.is_vendor
    
    @api.depends('customer_rank', 'supplier_rank')
    def _compute_rank(self):
        for rec in self:
            rec.is_customer = rec.customer_rank
            rec.is_vendor = rec.supplier_rank
    