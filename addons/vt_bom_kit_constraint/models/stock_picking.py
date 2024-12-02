import math
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    def button_validate(self):
        def check_if_same_qty(lst):
            return all(x == lst[0] for x in lst) if lst else True  # Returns True for an empty list
        
        moves = self.mapped("move_ids_without_package").filtered(
            lambda x: x.bom_line_id
        )
        boms = moves.mapped("bom_line_id.bom_id")
        for bom in boms:
            bom_moves = moves.filtered(lambda x: x.bom_line_id.bom_id == bom)
            if not check_if_same_qty(bom_moves.mapped('quantity')):
                print('not same')
                raise ValidationError(
                    _(
                        "You can't make a partial delivery of components of the "
                        "%s kit",
                        bom.product_tmpl_id.display_name,
                    )
                )
            else:
                print('same')
                
        res = super().button_validate()
        return res
    
    def button_populate_minimum_bom_qty(self):
        moves = self.mapped('move_ids_without_package').filtered(lambda x: x.bom_line_id)
        
        boms = moves.mapped('bom_line_id.bom_id')
        for bom in boms:
            bom_moves = moves.filtered(lambda x: x.bom_line_id.bom_id == bom)
            
            # Reset bom moves quantity so that we can correctly calculate the available quantity from stock quant
            for move in bom_moves:
                move.quantity = 0
            
            # Calculate minimum BOM qty based on available quantity from stock quant
            # Available quantity = on hand quantity - reserved quantity
            minimum_product_qty_dict = {}
            for move in bom_moves:
                stock_quant = self.env['stock.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id.usage', '=', 'internal'),
                ])
                
                available_qty = stock_quant.quantity - stock_quant.reserved_quantity
                available_bom_qty = math.floor(available_qty / move.bom_line_id.product_qty)
                bom_demand = math.floor(move.product_uom_qty / move.bom_line_id.product_qty)
                if available_bom_qty >= bom_demand:
                    available_bom_qty = bom_demand
                
                if not minimum_product_qty_dict or available_qty < minimum_product_qty_dict.get('available_qty'):
                    minimum_product_qty_dict.update({
                        'product_template_id': stock_quant.product_id.product_tmpl_id,
                        'available_qty': available_qty,
                        'available_bom_qty': available_bom_qty
                    })
                
            # Populate minimum BOM qty based on calculation above
            for move in bom_moves:
                move.quantity = move.bom_line_id.product_qty * minimum_product_qty_dict['available_bom_qty']