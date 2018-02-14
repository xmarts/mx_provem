## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, date, time,timedelta
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit ='sale.order'
    referency1 = fields.Char('Referencia 1')
    referency2 = fields.Char('Referencia 2')