from itertools import islice
from odoo import models, _
from odoo.addons.abp_utils.utils import format_currency_amount
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def button_sync_pricelist(self):
        for rec in self:
            for line in rec.order_line:
                line._compute_pricelist_item_id()
    
    def button_print_barcode(self):
        report_actions = []
        customer_product_refs = self.order_line.mapped('customer_product_ref')
        barcode = self.order_line.mapped('barcode')
        if 'Multiple pricelist item' in customer_product_refs or 'Multiple pricelist item' in barcode:
            raise ValidationError(_('Duplicate items found on pricelist item. Remove duplicated items from pricelist item to continue'))
        
        data = self._prepare_product_label_data(self)
        batch_size = 50  # Adjust the batch size as needed
        
        def chunks(iterable, size):
            it = iter(iterable)
            return iter(lambda: tuple(islice(it, size)), ())
        
        for batch in chunks(data, batch_size):
            action = self.env.ref('abp_pricelist.action_report_sales_product_barcode')\
                        .report_action(self, data={
                            'data': batch,
                            'name': 'TEST'
                        })
            report_actions.append(action)
            
        if len(report_actions) == 1: 
            return report_actions[0]
        elif len(report_actions) > 1:  
            return {
                'type': 'ir.actions.client',
                'tag': 'do_multi_print',
                'params': {
                    'reports': report_actions,
                }
            }
    
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            for line in doc.order_line:
                label_qty = line.pricelist_item_id.label_qty
                
                qty = 0
                if label_qty > 0:
                    qty = int(line.product_uom_qty) * label_qty
                else:
                    qty = int(line.product_uom_qty)
                    
                for _ in range(qty):
                    data.append({
                        'product_code': line.customer_product_code or line.product_template_id.default_code,
                        'product_name': line.product_id.name,
                        'barcode': line.barcode,
                        'price': format_currency_amount(line.retail_price or 0.0, doc.env.company.currency_id),
                    })
        return data
    
    # Had to overwrite to trigger depends (write) upon sale.order.line creation
    def _update_order_line_info(self, product_id, quantity, **kwargs):
        sol = self.order_line.filtered(lambda line: line.product_id.id == product_id)
        if sol:
            if quantity != 0:
                sol.product_uom_qty = quantity
            elif self.state in ['draft', 'sent']:
                price_unit = self.pricelist_id._get_product_price(
                    product=sol.product_id,
                    quantity=1.0,
                    currency=self.currency_id,
                    date=self.date_order,
                    **kwargs,
                )
                sol.unlink()
                return price_unit
            else:
                sol.product_uom_qty = 0
        elif quantity > 0:
            sol = self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': product_id,
                'product_uom_qty': quantity,
                'sequence': ((self.order_line and self.order_line[-1].sequence + 1) or 10),  # put it at the end of the order
            })
            # Modification start
            # To trigger depends (write)
            sol.product_uom_qty = quantity
            # Modification end
        return sol.price_unit
    