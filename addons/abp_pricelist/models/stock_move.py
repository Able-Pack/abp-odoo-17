from odoo import api, fields, models, _
from odoo.addons.abp_utils.utils import format_currency_amount


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    pricelist_item_id = fields.Many2one(comodel_name='product.pricelist.item', compute='_compute_pricelist_item_id', store=True)
    customer_product_ref = fields.Char(string='Customer Product Ref', compute='_compute_pricelist_item_id', store=True)
    barcode = fields.Char(string='EAN13', compute='_compute_pricelist_item_id', store=True)
    retail_price = fields.Float(string="Retail Price", compute='_compute_pricelist_item_id', store=True)
    
    @api.depends('product_id')
    def _compute_pricelist_item_id(self):
        data = []
        for line in self:
            pricelist_item = False
            line.pricelist_item_id = line.customer_product_ref = line.barcode = False
            if line.bom_line_id:
                if line.bom_line_id.bom_id not in [dt['bom_id'] for dt in data]:
                    pricelist_item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                        ('product_tmpl_id', '=', line.bom_line_id.bom_id.product_tmpl_id.id),
                    ])
            else:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                ])
                
            line.pricelist_item_id = pricelist_item
            line.customer_product_ref = pricelist_item.customer_product_ref
            line.barcode = pricelist_item.barcode
            line.retail_price = pricelist_item.retail_price or line.pricelist_item_id.fixed_price
    
    # Deprecated because we need to get the pricelist item matching the component's parent, not the component itself
    # @api.depends('product_id')
    # def _compute_pricelist_item_id(self):
    #     for rec in self:
    #         rec.pricelist_item_id = rec.customer_product_ref = rec.barcode = False
    #         rec.retail_price = 0.0
    #         if rec.product_id:
    #             pricelist_item = self.env['product.pricelist.item'].search([
    #                 ('pricelist_id', '=', rec.picking_id.partner_id.property_product_pricelist.id),
    #                 ('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id)
    #             ])
    #             if len(pricelist_item) == 1:
    #                 rec.pricelist_item_id = pricelist_item
    #                 rec.customer_product_ref = pricelist_item.customer_product_ref
    #                 rec.barcode = pricelist_item.barcode
    #                 rec.retail_price = pricelist_item.retail_price or rec.pricelist_item_id.fixed_price
    #             elif len(pricelist_item) == 0:
    #                 rec.customer_product_ref = rec.barcode = False
    #                 rec.retail_price = 0.0
    #             elif len(pricelist_item) > 1:
    #                 rec.customer_product_ref = rec.barcode = False
    #                 rec.retail_price = 0.0