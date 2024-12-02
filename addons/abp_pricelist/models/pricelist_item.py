from odoo import api, fields, models, tools


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    sequence = fields.Integer(string='Sequence')
    customer_product_ref = fields.Char()
    barcode = fields.Char(string='EAN13')
    label_qty = fields.Integer(string='Label Qty')
    retail_price = fields.Float()
    distributor_price = fields.Float(compute='_compute_distributor_price')
    base = fields.Selection(selection_add=[('retail_price', 'Retail Price')], ondelete={'retail_price': 'cascade'})
    rounding_option = fields.Selection([
        ('UP', 'Round Up'),
        ('HALF-UP', 'Half Up'),
        ('HALF-DOWN', 'Half Down'),
        ('HALF_EVEN', 'Half Even'),
        ('DOWN', 'Round Down'),
    ], default='DOWN')
    
    
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
    
    @api.depends('retail_price', 'price_discount', 'price_surcharge', 'price_round', 'rounding_option', 'base')
    def _compute_distributor_price(self):
        for rec in self:
            price = 0.0
            if rec.base == 'retail_price':
                # complete formula
                base_price = rec.retail_price
                price_limit = base_price
                price = (base_price - (base_price * (rec.price_discount / 100))) or 0.0
                if rec.price_round:
                    price = tools.float_round(price, precision_rounding=rec.price_round, rounding_method=rec.rounding_option)
                    
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
        
        
    # Overwrite
    # Add parameter rounding_method on float_round function call
    def _compute_price(self, product, quantity, uom, date, currency=None):
        """Compute the unit price of a product in the context of a pricelist application.
        
        Note: self and self.ensure_one()
        
        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param currency: currency (for the case where self is empty)
        
        :returns: price according to pricelist rule or the product price, expressed in the param
                  currency, the pricelist currency or the company currency
        :rtype: float
        """
        self and self.ensure_one()  # self is at most one record
        product.ensure_one()
        uom.ensure_one()
        
        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()
        
        # Pricelist specific values are specified according to product UoM
        # and must be multiplied according to the factor between uoms
        product_uom = product.uom_id
        if product_uom != uom:
            convert = lambda p: product_uom._compute_price(p, uom)
        else:
            convert = lambda p: p
            
        if self.compute_price == 'fixed':
            price = convert(self.fixed_price)
        elif self.compute_price == 'percentage':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price = (base_price - (base_price * (self.percent_price / 100))) or 0.0
        elif self.compute_price == 'formula':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            # complete formula
            price_limit = base_price
            price = (base_price - (base_price * (self.price_discount / 100))) or 0.0
            if self.price_round:
                # Before
                # price = tools.float_round(price, precision_rounding=self.price_round)
                # After
                price = tools.float_round(price, precision_rounding=self.price_round, rounding_method=self.rounding_option)
                
            if self.price_surcharge:
                price += convert(self.price_surcharge)
                
            if self.price_min_margin:
                price = max(price, price_limit + convert(self.price_min_margin))
                
            if self.price_max_margin:
                price = min(price, price_limit + convert(self.price_max_margin))
        else:  # empty self, or extended pricelist price computation logic
            price = self._compute_base_price(product, quantity, uom, date, currency)
            
        return price
    
    