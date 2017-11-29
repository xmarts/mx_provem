## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError

import shutil
import logging
_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit ='stock.quant'

    @api.one
    def _compute_standardprice(self):
        self.standard_price = self.product_id.standard_price
    standard_price= fields.Float(string="Costo", compute="_compute_standardprice", store=True)
