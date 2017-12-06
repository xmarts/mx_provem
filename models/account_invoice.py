## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, date, time,timedelta
from odoo.addons import decimal_precision as dp
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit ='account.invoice'
    amount_total = fields.Monetary(string='Total',
                                   store=True, readonly=True, compute='_compute_amount', digits=dp.get_precision('Product Price'))

class AccountInvoiceline(models.Model):
    _inherit = 'account.invoice.line'
    price_subtotal = fields.Monetary(string='Amount',
                                     store=True, readonly=True, compute='_compute_price',
                                     help="Total amount without taxes",  digits=dp.get_precision('Product Price'))