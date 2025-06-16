import math
from odoo import _, models
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    
    def button_validate(self):
        # Check if BOM lines are in correct multiples of their BoM quantities
        grouped_moves = defaultdict(list)
        bom_moves = self.mapped("move_ids_without_package").filtered(lambda m: m.bom_line_id)

        # Group by BoM
        for move in bom_moves:
            grouped_moves[move.bom_line_id.bom_id].append(move)

        for bom, moves in grouped_moves.items():
            ratios = set()
            for move in moves:
                bom_qty = move.bom_line_id.product_qty
                if bom_qty == 0:
                    continue  # skip invalid bom line
                ratio = move.quantity / bom_qty
                ratios.add(round(ratio, 6))  # avoid float error

            if len(ratios) > 1:
                raise UserError(_(
                    "Move lines for BoM [%s] are not in correct multiples to their BoM quantities."
                ) % bom.display_name)
                
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
                # print(move.product_id.product_tmpl_id.name, move.product_id.qty_available)
                # TODO: Use another way to get the WH/Stock
                # Eg. using a field to determine the main stock location (not consignment, etc)
                stock_quant = self.env['stock.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id.usage', '=', 'internal'),
                    ('location_id.name', 'ilike', 'stock'),
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