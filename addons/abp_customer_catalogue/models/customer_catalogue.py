from odoo import api, fields, models, _
from odoo.addons.abp_utils.utils import format_currency_amount


class CustomerCatalogue(models.Model):
    _name = "customer.catalogue"
    _desc = _name
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string="Name")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer", required=True)
    product_tmpl_id = fields.Many2one(comodel_name='product.template', related='product_id.product_tmpl_id')
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    customer_product_code = fields.Char(string='Customer Product Code')
    customer_product_ref = fields.Char(string='Customer Product Ref', compute='_compute_pricelist_item')
    barcode = fields.Char(string='EAN13', compute='_compute_pricelist_item')
    retail_price = fields.Float(compute='_compute_pricelist_item')
    
    # @api.depends('product_tmpl_id', 'customer_product_code', 'customer_product_ref')
    @api.depends('product_tmpl_id', 'customer_product_code')
    def _compute_display_name(self):
        for rec in self:
            name = rec.display_name
            if rec.customer_product_code:
                name = f'{rec.product_tmpl_id.display_name} [{rec.customer_product_code}]'
            else:
                name = f'{rec.product_tmpl_id.display_name}'
                
            rec.display_name = name
            
    # @api.depends('customer_product_ref')
    @api.depends('product_id')
    def _compute_pricelist_item(self):
        for rec in self:
            pricelist_item = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', rec.partner_id.property_product_pricelist.id),
                ('product_tmpl_id', '=', rec.product_tmpl_id.id),
                
                # If use customer product ref
                # ('customer_product_ref', '=', rec.customer_product_ref),
            ])
            
            if len(pricelist_item) == 1:
                rec.customer_product_ref = pricelist_item.customer_product_ref
                rec.barcode = pricelist_item.barcode
                rec.retail_price = pricelist_item.retail_price or pricelist_item.fixed_price
            elif len(pricelist_item) > 1:
                rec.customer_product_ref = rec.barcode = rec.retail_price = False
            else:
                rec.customer_product_ref = rec.barcode = rec.retail_price = False
                
            # If use customer product ref
            # rec.barcode = pricelist_item.barcode
            # rec.retail_price = pricelist_item.retail_price
            
            
    # Will be called from tree views
    def button_print_barcode(self):
        data = self._prepare_product_label_data(self)
        return self.env.ref('abp_customer_catalogue.action_report_customer_catalogue_product_barcode').report_action(self, data={'data': data})
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            data.append({
                'product_code': doc.customer_product_code or doc.product_tmpl_id.default_code,
                'product_name': doc.product_tmpl_id.name,
                'barcode': doc.barcode,
                'price': format_currency_amount(doc.retail_price or 0.0, doc.env.company.currency_id),
            })
        return data
            