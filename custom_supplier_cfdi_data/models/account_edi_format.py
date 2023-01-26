# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _l10n_mx_edi_get_common_cfdi_values(self, move):
        res = super(AccountEdiFormat, self)._l10n_mx_edi_get_common_cfdi_values(move)
        if move.company_id.x_commercial_partner_id:
            res["supplier"] = move.company_id.x_commercial_partner_id
        return res