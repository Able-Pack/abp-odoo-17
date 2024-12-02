from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    customer_product_ref = fields.Char(string='Customer Product Ref', compute='_compute_pricelist_item_id', store=True)
    barcode = fields.Char(string='EAN13', compute='_compute_pricelist_item_id', store=True)
    retail_price = fields.Float(string="Retail Price", compute='_compute_pricelist_item_id', store=True)
    
    # Override parent method
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        for rec in self:
            super()._compute_pricelist_item_id()
            rec.customer_product_ref = rec.barcode = False
            rec.retail_price = 0.0
            
            if rec.pricelist_item_id:
                rec.customer_product_ref = rec.pricelist_item_id.customer_product_ref
                rec.barcode = rec.pricelist_item_id.barcode
                rec.retail_price = rec.pricelist_item_id.retail_price or rec.pricelist_item_id.fixed_price
                
            # Manually search to product.pricelist.item to make sure if there is only single pricelist item record
            pricelist_item_temp = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', rec.order_id.partner_id.property_product_pricelist.id),
                ('product_tmpl_id', '=', rec.product_template_id.id)
            ])
            if len(pricelist_item_temp) > 1:
                rec.customer_product_ref = rec.barcode = 'Multiple pricelist item'
                rec.retail_price = 0.0