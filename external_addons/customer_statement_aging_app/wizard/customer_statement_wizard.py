from odoo import models, fields, api, _
from odoo.tools import date_utils
from odoo.addons.abp_utils.utils import format_currency_amount


class CustomerStatementWizard(models.TransientModel):
    _name = 'customer.statement.wizard'
    _description = "Customer Statement Wizard"
    #
    partner_ids = fields.Many2many('res.partner', string='Customer')
    invoice_ids = fields.Many2many('account.move', 'rel_invoice_wizard', 'wizard_id', 'invoice_id', string='Invoice')
    months = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
         ('7', 'July'),
         ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], default='1')
    aging_by = fields.Selection([('due', 'Due Date'), ('invoice', 'Invoice Date')], default='due')
    previous_year = fields.Boolean(string='Print Previous Year')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    @api.model
    def default_get(self, fields):
        res = super(CustomerStatementWizard, self).default_get(fields)
        partner_ids = self.env['res.partner'].browse(self._context.get('active_ids'))
        res['partner_ids'] = [(6, 0, partner_ids.ids)]
        return res

    @api.onchange('months', 'aging_by', 'previous_year')
    def onchange_get_invoice_data(self):
        for rec in self:
            month = 1
            if rec.months == '1':
                month = 1
            elif rec.months == '2':
                month = 2
            elif rec.months == '3':
                month = 3
            elif rec.months == '4':
                month = 4
            elif rec.months == '5':
                month = 5
            elif rec.months == '6':
                month = 6
            elif rec.months == '7':
                month = 7
            elif rec.months == '8':
                month = 8
            elif rec.months == '9':
                month = 9
            elif rec.months == '10':
                month = 10
            elif rec.months == '11':
                month = 11
            elif rec.months == '12':
                month = 12
            if rec.aging_by == 'due':
                if rec.previous_year:
                    now_date = fields.Date.today().replace(month=month, day=1)
                    year = now_date.year - 1
                    start_date = now_date.replace(year=year)
                    end_date = date_utils.end_of(start_date, "month")
                    invoice_ids = self.env['account.move'].search(
                        [('partner_id', 'in', rec.partner_ids.ids), ('invoice_date_due', '>=', start_date),
                         ('invoice_date_due', '<=', end_date), ('move_type', 'in', ('out_invoice', 'out_refund')),
                         ('state', '=', 'posted'),
                         ('amount_residual', '>', 0)])
                    rec.invoice_ids = [(6, 0, invoice_ids.ids)]
                else:
                    start_date = fields.Date.today().replace(month=month, day=1)
                    end_date = date_utils.end_of(start_date, "month")
                    invoice_ids = self.env['account.move'].search(
                        [('partner_id', 'in', rec.partner_ids.ids), ('invoice_date_due', '>=', start_date),
                         ('invoice_date_due', '<=', end_date), ('move_type', 'in', ('out_invoice', 'out_refund')),
                         ('state', '=', 'posted'),
                         ('amount_residual', '>', 0)])
                    rec.invoice_ids = [(6, 0, invoice_ids.ids)]
            else:
                if rec.previous_year:
                    now_date = fields.Date.today().replace(month=month, day=1)
                    year = now_date.year - 1
                    start_date = now_date.replace(year=year)
                    end_date = date_utils.end_of(start_date, "month")
                    invoice_ids = self.env['account.move'].search(
                        [('partner_id', 'in', rec.partner_ids.ids), ('invoice_date', '>=', start_date),
                         ('state', '=', 'posted'),
                         ('invoice_date', '<=', end_date), ('move_type', 'in', ('out_invoice', 'out_refund')),
                         ('amount_residual', '>', 0)])
                    rec.invoice_ids = [(6, 0, invoice_ids.ids)]
                else:
                    start_date = fields.Date.today().replace(month=month, day=1)
                    end_date = date_utils.end_of(start_date, "month")
                    invoice_ids = self.env['account.move'].search(
                        [('partner_id', 'in', rec.partner_ids.ids), ('invoice_date', '>=', start_date),
                         ('state', '=', 'posted'),
                         ('invoice_date', '<=', end_date), ('move_type', 'in', ('out_invoice', 'out_refund')),
                         ('amount_residual', '>', 0)])
                    rec.invoice_ids = [(6, 0, invoice_ids.ids)]

    def action_print_report(self):
        for rec in self:
            return self.env.ref('customer_statement_aging_app.action_customer_statement_report').report_action(self)

    def action_send(self):
        for rec in self:
            template_id = self.env.ref('customer_statement_aging_app.customer_statement_mail_template').id
            template = self.env['mail.template'].browse(template_id)
            for partner_id in rec.invoice_ids.mapped('partner_id'):
                body_html = 'Your Account Statement is Following ' + '<br/>'
                body_html += '<table><tr><th style= "border:1px solid black;padding:5px;">Invoice No</th><th style= ' \
                             '"border:1px solid black;padding:5px;">Invoice date</th><th style= "border:1px solid ' \
                             'black;padding:5px;">Due Date</th><th style= "border:1px solid ' \
                             'black;padding:5px;">Invoice Amount</th><th style= "border:1px solid ' \
                             'black;padding:5px;">Paid Amount</th><th style= "border:1px solid ' \
                             'black;padding:5px;">Due Amount</th></tr> '
                for invoice_id in rec.invoice_ids:
                    if invoice_id.partner_id == partner_id:
                        paid_amount = invoice_id.amount_total - invoice_id.amount_residual
                        body_html += '<tr><td style= "border:1px solid black;padding:5px;">' + invoice_id.name + '</td>'
                        body_html += '<td style= "border:1px solid black;padding:5px;">' + str(
                            invoice_id.invoice_date) + '</td>'
                        body_html += '<td style= "border:1px solid black;padding:5px;">' + str(
                            invoice_id.invoice_date_due) + '</td>'
                        body_html += '<td style= "border:1px solid black;padding:5px;">' + str(
                            round(invoice_id.amount_total)) + '</td>'
                        body_html += '<td style= "border:1px solid black;padding:5px;">' + str(
                            round(paid_amount, 2)) + '</td>'
                        body_html += '<td style= "border:1px solid black;padding:5px;">' + str(
                            round(invoice_id.amount_residual)) + '</td>'
                        body_html += '</tr>'
                        # body_html += 'Thank you'
                        # body_html += '<br/>' + self.user_id.name + (self.env.user.company_id.name)
                body_html += '</table>'
                template.body_html = body_html
                template.email_to = partner_id.email
                template.sudo().send_mail(self.id, force_send=True)
                
    def format_currency_amount(self, amount, currency_id=False):
        return format_currency_amount(amount, currency_id)
