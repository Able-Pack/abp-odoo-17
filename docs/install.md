# IMPORTANT NOTES
# abp_pricelist must be installed before abp_customer_catalogue 
# abp_pricelist must be upgraded also before abp_customer_catalogue 

# ablepack modules
install abp_utils
# install abp_base
install abp_report
install abp_accounting
install abp_payroll
install abp_pricelist
install abp_contact
install abp_sale
install abp_salesperson_dashboard
install abp_customer_catalogue
install abp_inventory
install abp_mrp

# external modules
install bi_invoice_backdate
install order_line_sequences
install customer_statement_aging_app
install dev_sales_commission
install muk_web_colors
install one2many_search_widget
install reset_journal_entries
install sttl_prevent_auto_save
install fx_hide_action_menu
install purchase_down_payment
install web_chatter_position_cr
install deltatech_stock_negative

# ablepack modules
# should be installed last to implement able pack's security (reset app menu groups)
install abp_security

# odoo default modules
# install web
# install website
install website_sale
# install sale
install contacts
# install point_of_sale
# install account_accountant
# install hr_expense
# install stock
# install mrp
# install purchase
# install hr
install web_studio
install partner_commission

