# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    # QR image field for invoice display
    invoice_qr_image = fields.Binary(
        string='Invoice QR Image',
        help='QR code image to display on customer invoices below company information'
    )
