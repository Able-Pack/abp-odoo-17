# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class salecommissionreport(models.Model):
    _name = "sale.commission.report"
    _description = "Sales Commission Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'


    commission_id = fields.Many2one('sale.commission', 'Commission #', readonly=True)
    name = fields.Char('Source Document', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    commission_date = fields.Datetime('Commission Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    amount = fields.Float('Commission Amount', readonly=True)
    user_type = fields.Selection([('sale_person','Sales Person'),('sale_manager','Sales Manager')], string='User Type', readonly=True)
    
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('paid','Paid'),('cancel','Cancel')], 
                                string='State', readonly=True)
    
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            min(l.id) as id,
            l.user_type as user_type,
            sum(l.amount) as amount,
            count(*) as nbr,
            l.origin as name,
            s.date as date,
            l.date as commission_date,
            s.state as state,
            s.user_id as user_id,
            s.company_id as company_id,
            s.id as commission_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                sale_commission_line l
                      join sale_commission s on (l.commission_id=s.id)
                %s
        """ % from_clause

        groupby_ = """
            l.user_type,
            l.origin,
            l.commission_id,
            l.origin,
            s.user_id,
            s.company_id,
            l.date,
            s.date,
            s.id %s
        """ % (groupby)

        return '%s (SELECT %s FROM %s GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

