from odoo import models, fields


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    barcode = fields.Char(string='EAN13')
    label_qty = fields.Integer(string='Label Qty')
    
    # Will be called from tree views
    def button_print_barcode(self):
        data = self._prepare_product_label_data(self)
        return self.env.ref('abp_pricelist.action_report_pricelist_item_product_barcode').report_action(self, data={'data': data})
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            data.append({
                'product_name': doc.product_tmpl_id.name,
                'barcode': doc.barcode,
            })
        return data
    