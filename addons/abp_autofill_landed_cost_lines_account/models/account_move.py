from odoo import models, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def button_create_landed_costs(self):
        res = super().button_create_landed_costs()
        stock_landed_cost_lines = self.env['stock.landed.cost.lines'].search([
                                        ('cost_id', '=', res['res_id'])
                                    ])
        for line in stock_landed_cost_lines:
            line.write({
                'account_id': line.product_id.property_account_expense_id
            })
        return res