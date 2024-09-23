from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    show_all_product = fields.Boolean(string='Show all products?')
    
    def action_confirm(self):
        partner_id = self.partner_id
        new_customer_catalogues = self._create_customer_catalogue()
        if new_customer_catalogues:
            self._send_email(new_customer_catalogues, partner_id)
        return super().action_confirm()
    
    def _create_customer_catalogue(self):
        result = []
        line_product_template_ids = self.order_line.mapped('product_template_id').mapped('id')
        customer_catalogue_model = self.env['customer.catalogue']
        customer_catalogue_ids = customer_catalogue_model.search([
            ('product_tmpl_id', 'in', line_product_template_ids),
            ('partner_id', '=', self.partner_id.id),
        ])
        customer_catalogue_product_tmpl_ids = customer_catalogue_ids.mapped('product_tmpl_id').mapped('id')
        for line in self.order_line:
            if line.product_template_id.id not in customer_catalogue_product_tmpl_ids:
                values = {
                    'partner_id': self.partner_id.id,
                    'product_id': line.product_id.id,
                    'customer_product_code': line.customer_product_code,
                    'customer_product_ref': line.customer_product_ref,
                }
                # create new customer catalogue record
                customer_catalogue_model.create(values)
                # include product template name and price unit in the email but not for the customer catalogue values
                values.update({
                    'product_tmpl_name': line.product_template_id.name,
                    'price_unit': line.price_unit
                })
                result.append(values)
                
        return result
    
    @api.model
    def _send_email(self, new_customer_catalogues, partner_id):
        subject = 'Customer Catalogue: New Records'
        
        body_html = f"""
            <p>Hello,</p>
            <p>A new customer catalogue for partner {partner_id.name} has been created with the following details:</p>
            
            <table border="1" cellpadding="5" cellspacing="0">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Product</th>
                        <th>Customer Product Code</th>
                        <th>Customer Product Ref</th>
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
                    <td>{item.get('customer_product_code', '-')}</td>
                    <td>{item.get('customer_product_ref', '-')}</td>
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
        
        # Create the mail.message record
        mail_values = {
            'subject': subject,
            'body_html': body_html,
            'email_to': 'victorimannuel21@gmail.com', # TODO: SET EMAIL TO AND FROM
            'email_from': self.env.user.email_formatted,
        }
        mail_id = self.env['mail.mail'].create(mail_values)
        
        # Send the email
        mail_id.send()
        
        
    def _get_product_catalog_additional_domain(self):
        order = self
        if not order.show_all_product:
            customer_catalogue = self.env['customer.catalogue'].search([
                ('partner_id', '=', order.partner_id.id)
            ])
            product_ids = customer_catalogue.mapped('product_id').mapped('id')
            additional_domain = [('id', 'in', product_ids)]
            return additional_domain
            
            
    def _get_product_catalog_domain(self):
        result = super()._get_product_catalog_domain()
        
        additional_domain = self._get_product_catalog_additional_domain()
        if additional_domain:
            result += additional_domain
            
        return result