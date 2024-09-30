from odoo import api, fields, models, tools


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    barcode = fields.Char(string='EAN13')
    label_qty = fields.Integer(string='Label Qty')
    retail_price = fields.Monetary()
    distributor_price = fields.Monetary(compute='_compute_distributor_price')
    base = fields.Selection(selection_add=[('retail_price', 'Retail Price')], ondelete={'retail_price': 'cascade'})
    
    # Will be called from tree views
    def button_print_barcode(self):
        data = self._prepare_product_label_data(self)
        return self.env.ref('abp_pricelist.action_report_pricelist_item_product_barcode').report_action(self, data={'data': data})
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            data.append({
                'product_code': doc.product_tmpl_id.default_code,
                'product_name': doc.product_tmpl_id.name,
                'barcode': doc.barcode,
                'price': doc.price or 0.0,
            })
        return data
    
    @api.depends('retail_price', 'price_discount', 'price_surcharge', 'price_round')
    def _compute_distributor_price(self):
        for rec in self:
            discounted_price = rec.retail_price * (100-rec.price_discount) / 100
            extra_price = rec.price_surcharge
            computed_price = discounted_price + extra_price
            if rec.price_round:
                computed_price = tools.float_round(computed_price, precision_rounding=rec.price_round)
            rec.distributor_price = computed_price
    
    def _compute_base_price(self, product, quantity, uom, date, currency):
        for rec in self:
            # Directly use retail price if the type is pricelist item is based on Retail Price
            if rec.base == 'retail_price':
                # Return this so that it will automatically computed in sale order
                price = rec.retail_price
                return price
            else:
                return super()._compute_base_price(product, quantity, uom, date, currency)