from odoo import models, _
from odoo.addons.abp_utils.utils import format_currency_amount


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    def button_print_barcode(self):
        data = self._prepare_product_label_data(self)
        return self.env.ref('abp_pricelist.actions_report_stock_picking_product_barcode').report_action(self, data={'data': data})
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            for line in doc.move_ids:
                label_qty = line.pricelist_item_id.label_qty
                qty = int(line.product_uom_qty) * label_qty if label_qty > 0 else int(line.product_uom_qty)
                
                for _ in range(qty):
                    data.append({
                        'product_code':line.product_id.default_code,
                        'product_name': line.product_id.name,
                        'barcode': line.barcode,
                        'price': format_currency_amount(line.retail_price or 0.0, doc.env.company.currency_id),
                    })
        return data