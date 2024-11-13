from odoo import api, models, _


class ProductProduct(models.Model):
    _inherit = 'product.template'
    
    def write(self, vals):
        res = super().write(vals)
        
        if 'standard_price' in vals:
            for bom_line in self.bom_line_ids:
                bom_line.bom_id.product_tmpl_id.action_bom_cost()
                
            # Compute all product variants, but actually unnecessary 
            # because the requirement is only to update bom's parent product cost wherever the bom line's product cost changed
            # products = self.filtered(lambda t: t.product_variant_count == 1 and len(t.bom_line_ids) > 0)
            # for product in products.mapped('product_variant_id'):
            #     for bom_line in product.bom_line_ids:
            #         bom_line.bom_id.product_tmpl_id.action_bom_cost()
            
        return res
    
    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    def write(self, vals):
        res = super().write(vals)
        
        if 'standard_price' in vals:
            for bom_line in self.bom_line_ids:
                bom_line.bom_id.product_tmpl_id.action_bom_cost()
                
        return res
    
    