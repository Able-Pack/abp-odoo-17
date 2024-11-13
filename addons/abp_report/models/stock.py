from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _get_consignment_memo_lines(self):
        values = []
        for move in self.move_ids:
            if move.bom_line_id:
                if move.bom_line_id.bom_id.product_tmpl_id.name not in [val['product_name'] for val in values]:
                    pricelist_item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                        ('product_tmpl_id', '=', move.bom_line_id.bom_id.product_tmpl_id.id),
                    ])
                    values.append({
                        'product_name': move.bom_line_id.bom_id.product_tmpl_id.name,
                        'product_code': move.bom_line_id.bom_id.product_tmpl_id.default_code,
                        'quantity': move.quantity,
                        'uom': move.product_uom.name,
                        'retail_price': pricelist_item.retail_price,
                    })
            else:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                    ('product_tmpl_id', '=', move.product_id.product_tmpl_id.id),
                ])
                values.append({
                    'product_name': move.product_id.name,
                    'product_code': move.product_id.default_code,
                    'quantity': move.quantity,
                    'uom': move.product_uom.name,
                    'retail_price': pricelist_item.retail_price,
                })
                
        return values
        
        
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    # Use customer catalogue fields, but should not depends to abp_customer_catalogue module because of circular dependency
    def _get_customer_catalogue_values(self, partner_id):
        customer_catalogue = partner_id.customer_catalogue_ids.filtered(lambda x: x.product_id == self.product_id)
        values = {
            'customer_product_code': customer_catalogue.customer_product_code,
            'customer_product_ref': customer_catalogue.customer_product_ref,
            'retail_price': customer_catalogue.retail_price,
        }
        return values