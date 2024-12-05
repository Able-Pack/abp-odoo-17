from odoo import models, _


class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    def create(self, vals):
        res = super().create(vals)
        
        product = self.env['product.template'].browse(vals.get('product_tmpl_id'))
        product.action_bom_cost()
                
        return res
    
    def write(self, vals):
        res = super().write(vals)
        
        if vals.get('bom_line_ids'):
            self.product_tmpl_id.action_bom_cost()
                
        return res