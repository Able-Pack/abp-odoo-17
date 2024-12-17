import math
from odoo import models, _
from odoo.addons.abp_utils.utils import format_currency_amount, chunks
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def button_sync_pricelist(self):
        for rec in self:
            for line in rec.move_ids:
                line._compute_pricelist_item_id()
    
    def button_print_barcode(self):
        report_actions = []
        customer_product_refs = self.move_ids.mapped('customer_product_ref')
        barcode = self.move_ids.mapped('barcode')
        if 'Multiple pricelist item' in customer_product_refs or 'Multiple pricelist item' in barcode:
            raise ValidationError(_('Duplicate items found on pricelist item. Remove duplicated items from pricelist item to continue'))
        
        data = self._prepare_product_label_data(self)
        batch_size = 50  # Adjust the batch size as needed
        page_count = math.ceil((len(data) / batch_size)) # Use this because can't use len on chunked_data
        
        for i, batch in enumerate(chunks(data, batch_size)):
            action = self.env.ref('abp_pricelist.actions_report_stock_picking_product_barcode')\
                        .report_action(self, data={
                            'data': batch,
                            'filename': f'{self.name} ({(i+1)} of {page_count})'
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
            
    # def _prepare_product_label_data(self, docs):
    #     data = []
    #     for doc in docs:
    #         for line in doc.move_ids:
    #             label_qty = line.pricelist_item_id.label_qty
    #             qty = int(line.quantity) * label_qty if label_qty > 0 else int(line.quantity)
                
    #             for _ in range(qty):
    #                 data.append({
    #                     'product_code': line.product_tmpl_id.default_code,
    #                     'product_name': line.product_id.name,
    #                     'barcode': line.barcode,
    #                     'barcode_binary': False,
    #                     'price': format_currency_amount(line.retail_price or 0.0, doc.env.company.currency_id),
    #                 })
    #     return data
    
    # Deprecated, because we just use values from line
    def _prepare_product_label_data(self, docs):
        data = []
        for doc in docs:
            for line in doc.move_ids:
                pricelist_item = False
                
                if line.bom_line_id:
                    if line.bom_line_id.bom_id not in [dt['bom_id'] for dt in data]:
                        
                        pricelist_item = self.env['product.pricelist.item'].search([
                            ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                            ('product_tmpl_id', '=', line.bom_line_id.bom_id.product_tmpl_id.id),
                        ])
                        
                        label_qty = pricelist_item.label_qty
                        qty = int(line.quantity) * label_qty if label_qty > 0 else int(line.quantity)
                        for _ in range(qty):
                            data.append({
                                'bom_id': line.bom_line_id.bom_id,
                                'product_name': pricelist_item.product_tmpl_id.name,
                                'product_code':pricelist_item.product_tmpl_id.default_code,
                                'barcode': pricelist_item.barcode,
                                'barcode_binary': False,
                                'price': format_currency_amount(pricelist_item.retail_price or pricelist_item.fixed_price or 0.0, doc.env.company.currency_id),
                            })
                            
                else:
                    pricelist_item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', self.partner_id.property_product_pricelist.id),
                        ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                    ])
                    
                    label_qty = pricelist_item.label_qty
                    qty = int(line.quantity) * label_qty if label_qty > 0 else int(line.quantity)
                    for _ in range(qty):
                        data.append({
                            'bom_id': False,
                            'product_name': pricelist_item.product_tmpl_id.name,
                            'product_code':pricelist_item.product_tmpl_id.default_code,
                            'barcode': pricelist_item.barcode,
                            'barcode_binary': False,
                            'price': format_currency_amount(pricelist_item.retail_price or pricelist_item.fixed_price or 0.0, doc.env.company.currency_id),
                        })
                        
        return data