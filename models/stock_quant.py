## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError

import shutil
import logging
from lxml import etree
import datetime
import time
_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit ='stock.quant'

    @api.one
    def _compute_standardprice(self):
        self.standard_price = self.product_id.standard_price
    standard_price= fields.Float(string="Costo", compute="_compute_standardprice", store=True)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_partners_in_need_of_action_and_update(self):
        company_id = self.env.user.company_id
        context = self.env.context
        cr = self.env.cr
        date = 'date' in context and context['date'] or time.strftime('%Y-%m-%d')

        cr.execute(
            "SELECT l.partner_id, l.followup_line_id, l.date_maturity, l.date, l.id, fl.delay " \
            "FROM account_move_line AS l " \
            "LEFT JOIN account_account AS a " \
            "ON (l.account_id=a.id) " \
            "LEFT JOIN account_account_type AS act " \
            "ON (a.user_type_id=act.id) " \
            "LEFT JOIN account_followup_followup_line AS fl " \
            "ON (l.followup_line_id=fl.id) " \
            "WHERE (l.reconciled IS FALSE) " \
            "AND (act.type='receivable') " \
            "AND (l.partner_id is NOT NULL) " \
            "AND (a.deprecated='f') " \
            "AND (l.debit > 0) " \
            "AND (l.company_id = %s) " \
            "AND (l.blocked IS FALSE) " \
            "ORDER BY l.date", (
            company_id.id,))  # l.blocked added to take litigation into account and it is not necessary to change follow-up level of account move lines without debit
        move_lines = cr.fetchall()
        old = None
        fups = {}
        fup_id = 'followup_id' in context and context['followup_id'] or self.env['account_followup.followup'].search(
            [('company_id', '=', company_id.id)]).id
        if not fup_id:
            raise Warning(_('No follow-up is defined for the company "%s".\n Please define one.') % company_id.name)

        if not fup_id:
            return {}

        current_date = datetime.date(*time.strptime(date, '%Y-%m-%d')[:3])
        cr.execute(
            "SELECT * " \
            "FROM account_followup_followup_line " \
            "WHERE followup_id=%s " \
            "ORDER BY delay", (fup_id,))

        # Create dictionary of tuples where first element is the date to compare with the due date and second element is the id of the next level
        for result in cr.dictfetchall():
            delay = datetime.timedelta(days=result['delay'])
            fups[old] = (current_date - delay, result['id'])
            old = result['id']

        fups[old] = (current_date - delay, old)

        result = {}

        partners_to_skip = self.env['res.partner'].search([('payment_next_action_date', '>', date)])

        # Fill dictionary of accountmovelines to_update with the partners that need to be updated
        for partner_id, followup_line_id, date_maturity, date, id, delay in move_lines:
            if not partner_id or partner_id in partners_to_skip.ids:
                continue
            if followup_line_id not in fups:
                continue
            if date_maturity:
                if date_maturity <= fups[followup_line_id][0].strftime('%Y-%m-%d'):
                    if partner_id not in result:
                        result.update({partner_id: (fups[followup_line_id][1], delay)})
                    elif result[partner_id][1] == delay or result[partner_id][1] < delay:
                        result[partner_id] = (fups[followup_line_id][1], delay)
            elif date and date <= fups[followup_line_id][0].strftime('%Y-%m-%d'):
                if partner_id not in result:
                    result.update({partner_id: (fups[followup_line_id][1], delay)})
                elif result[partner_id][1] < delay:
                    result[partner_id] = (fups[followup_line_id][1], delay)
        return result
