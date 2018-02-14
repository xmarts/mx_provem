## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, date, time,timedelta
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit ='account.invoice'
    amount_total = fields.Monetary(string='Total',
                                   store=True, readonly=True, compute='_compute_amount', digits=dp.get_precision('Product Price'))
    #tipo_cambio =fields.Float(string='Tipo de cambio', store=True, readonly=True, compute='_compute_change',help="Tipo de cambio",  digits=2)

    #@api.one
    #@api.depends('currency_id')
    #def _compute_change(self):
    #    currency = self.currency_id
    #    rate = self.env['res.currency.rate'].search([('currency_id','=',currency.id)])
    #    self.tipo_cambio = self.price_unit + (self.price_unit * 0.16)
    sale_id = fields.Many2one('sale.order', string="venta",  compute='_compute_order', store=True)
    @api.one
    @api.depends('origin')
    def _compute_order(self):
        if self.origin is not False:
            valor = self.origin[0:2]
            if valor == 'SO':
                order = self.env['sale.order'].search([('name','=',self.origin)], limit =1)
                self.sale_id = order.id


class AccountInvoiceline(models.Model):
    _inherit = 'account.invoice.line'
    price_subtotal = fields.Monetary(string='Amount',
                                     store=True, readonly=True, compute='_compute_price',
                                     help="Total amount without taxes",  digits=dp.get_precision('Product Price'))
    price_untaxed = fields.Monetary(string='Precio untaxed',
                                     store=True, readonly=True, compute='_compute_prices',
                                     help="Total amount without taxes",  digits=dp.get_precision('Product Price'))

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice')
    def _compute_prices(self):
        self.price_untaxed = self.price_unit + (self.price_unit * 0.16)
