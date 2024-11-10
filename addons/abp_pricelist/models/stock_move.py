from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    pricelist_item_id = fields.Many2one(comodel_name='product.pricelist.item', compute='_compute_pricelist_item_id')
    customer_product_ref = fields.Char(string='Customer Product Ref', compute='_compute_pricelist_item_id')
    barcode = fields.Char(string='EAN13', compute='_compute_pricelist_item_id')
    retail_price = fields.Float(string="Retail Price", compute='_compute_pricelist_item_id')
    
    @api.depends('product_id')
    def _compute_pricelist_item_id(self):
        for rec in self:
            rec.pricelist_item_id = rec.customer_product_ref = rec.barcode = False
            rec.retail_price = 0.0
            if rec.product_id:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', rec.picking_id.partner_id.property_product_pricelist.id),
                    ('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id)
                ])
                rec.pricelist_item_id = pricelist_item
                rec.customer_product_ref = pricelist_item.customer_product_ref
                rec.barcode = pricelist_item.barcode
                rec.retail_price = pricelist_item.retail_price or rec.pricelist_item_id.fixed_price