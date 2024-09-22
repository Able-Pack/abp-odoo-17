from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def button_print_barcode(self):
        data = self._prepare_product_label_data(self)
        return self.env.ref('abp_pricelist.action_report_sales_product_barcode').report_action(self, data={'data': data})
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            for line in doc.order_line:
                barcode = line.barcode
                label_qty = line.pricelist_item_id.label_qty
                
                qty = 0
                if label_qty > 0:
                    qty = int(line.product_uom_qty) * label_qty
                else:
                    qty = int(line.product_uom_qty)
                    
                for _ in range(qty):
                    data.append({
                        'product_name': line.product_id.name,
                        'barcode': barcode,
                    })
        return data
    