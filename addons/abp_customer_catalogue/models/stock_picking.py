import json
from lxml import etree
from odoo import api, fields, models, _
from odoo.addons.abp_utils import views as utils
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_admin_product = fields.Boolean(string='Show admin products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_specific_product = fields.Boolean(string='Show customer-specific products?', default=False)
    has_new_customer_catalogue = fields.Boolean(default=False)
    new_customer_catalogue_json = fields.Json()
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("form"):
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_admin_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_admin_product']/.."])
                
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_base_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_base_product']/.."])
                
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_customer_specific_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_customer_specific_product']/.."])
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
    
    def write(self, vals):
        if 'show_admin_product' in vals:
            if vals['show_admin_product'] == True:
                vals['show_base_product'] = vals['show_customer_specific_product'] = False
                
        if 'show_base_product' in vals:
            if vals['show_base_product'] == True:
                vals['show_admin_product'] = vals['show_customer_specific_product'] = False
                
        if 'show_customer_specific_product' in vals:
            if vals['show_customer_specific_product'] == True:
                vals['show_admin_product'] = vals['show_base_product'] = False
                
        return super().write(vals)
    
    def button_validate(self):
        res = super().button_validate()
        self._create_customer_catalogue()
        if self.has_new_customer_catalogue:
            self.button_notify_catalogue_creation()
        return res
    
    @api.onchange('move_ids_without_package')
    def _onchange_move_ids_without_package(self):
        self.show_base_product = False
        self.show_customer_specific_product = False
        
    def _create_customer_catalogue(self):
        result = []
        
        products = []
        for move in self.move_ids_without_package:
            if move.bom_line_id:
                products.append(move.bom_line_id.bom_id.product_tmpl_id)
            else:
                products.append(move.product_id.product_tmpl_id)
        
        draft_new_customer_catalogue = []
        for product in products:
            customer_catalogue_ids = self.env['customer.catalogue'].search([
                ('product_tmpl_id', '=', product.id),
                ('partner_id', '=', self.partner_id.id),
            ])
            if not customer_catalogue_ids:
                values = {
                    'partner_id': self.partner_id.id,
                    'product_id': product.product_variant_ids[0].id
                }
                draft_new_customer_catalogue.append(values)
                # create new customer catalogue record
                self.env['customer.catalogue'].create(values)
                # include product template name and price unit in the email but not for the customer catalogue values
                values.update({
                    'barcode': False,
                    'product_tmpl_name':product.display_name,
                    'price_unit': False
                })
                result.append(values)
        
        if result:
            self.has_new_customer_catalogue = True
            self.new_customer_catalogue_json = result
        
        return result
    
    def button_notify_catalogue_creation(self):
        self._notify_catalogue_creation(self.new_customer_catalogue_json, self.partner_id)
    
    @api.model
    def _notify_catalogue_creation(self, new_customer_catalogues, partner_id):
        subject = 'Customer Catalogue: New Records'
        
        body_html = f"""
            <p>Hello,</p>
            <p>A new customer catalogue for partner <strong>{partner_id.name}</strong> has been created with the following details:</p>
            
            <table border="1" cellpadding="5" cellspacing="0">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Product</th>
                        <th>EAN13</th>
                        <th>Customer Product Code</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add each item to the table
        for idx, item in enumerate(new_customer_catalogues):
            body_html += f"""
                <tr>
                    <td style="text-align: center;">{idx+1}</td>
                    <td>{item.get('product_tmpl_name', '-')}</td>
                    <td>{item.get('barcode', '-')}</td>
                    <td>{item.get('customer_product_code', '-')}</td>
                    <td>{item.get('price_unit', '-')}</td>
                </tr>
            """
        
        body_html += """
                </tbody>
            </table>
            <br/>
            <p>Best regards,
            <br/>Able Pack Ltd</p>
        """
        
        email_to = self.env["ir.config_parameter"].sudo().get_param("abp_customer_catalogue.newly_created_customer_catalogue_target_email")
        outgoing_mail_server = self.env['ir.mail_server'].sudo().search([], order='sequence', limit=1)
        # Create the mail.message record
        mail_values = {
            'subject': subject,
            'body_html': body_html,
            'email_to': email_to,
            'email_from': outgoing_mail_server.smtp_user or '',
        }
        mail_id = self.env['mail.mail'].sudo().create(mail_values)
        
        try:
            # Send the email
            mail_id.send()
            # After sending, set the boolean field back to False
            self.has_new_customer_catalogue = False
        except Exception as e:
            raise UserError(_(str(e)))