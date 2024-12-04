from odoo import api, models, _


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    @api.model
    def create(self, vals):
        # Trigger recompute on linked customer.catalogue records
        # Use filtered function because non-stored field can't be searched using odoo ORM (property_product_pricelist)
        matching_partners = self.env['res.partner'].search([]).filtered(lambda x: x.property_product_pricelist.id == vals['pricelist_id']).ids
        related_catalogues = self.env['customer.catalogue'].search([
            ('partner_id', 'in', matching_partners),
            ('product_tmpl_id.id', '=', vals['product_tmpl_id'])
        ])
        for catalogue in related_catalogues:
            catalogue.barcode = vals.get('barcode', False)
            catalogue.customer_product_ref = vals.get('customer_product_ref', False)
            
        return super().create(vals)
    
    def write(self, vals):
        res = super().write(vals)
        # Trigger recompute on linked customer.catalogue records
        related_catalogues = self.env['customer.catalogue'].search([
            ('pricelist_item_id', 'in', self.ids)
        ])
        if related_catalogues:
            related_catalogues._compute_pricelist_item()
        
        return res