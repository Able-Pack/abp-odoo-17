from odoo import api, fields, models, tools


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    barcode = fields.Char(string='EAN13')
    label_qty = fields.Integer(string='Label Qty')
    retail_price = fields.Float()
    distributor_price = fields.Float(compute='_compute_distributor_price')
    base = fields.Selection(selection_add=[('retail_price', 'Retail Price')], ondelete={'retail_price': 'cascade'})
    customer_product_ref = fields.Char()
    
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
            price = 0.0
            if rec.base == 'retail_price':
                # complete formula
                base_price = rec.retail_price
                price_limit = base_price
                price = (base_price - (base_price * (rec.price_discount / 100))) or 0.0
                if rec.price_round:
                    price = tools.float_round(price, precision_rounding=rec.price_round)
                    
                if rec.price_surcharge:
                    price += rec.price_surcharge
                    
                if rec.price_min_margin:
                    price = max(price, price_limit + rec.price_min_margin)
                    
                if rec.price_max_margin:
                    price = min(price, price_limit + rec.price_max_margin)
                    
            rec.distributor_price = price
    
    def _compute_base_price(self, product, quantity, uom, date, currency):
        # Directly use retail price if the type is pricelist item is based on Retail Price
        if self.base == 'retail_price':
            # Return this so that it will automatically computed in sale order
            price = self.retail_price or 0.0
            return float(price)
        else:
            return super()._compute_base_price(product, quantity, uom, date, currency)