from odoo import _, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def unlink(self):
        for picking in self:
            if picking.state not in ('draft'):
                raise ValidationError(_('Deleting lines only allowed in draft state'))
        return super().unlink()