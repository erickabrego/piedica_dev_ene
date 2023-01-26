from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    client_id = fields.Many2one('res.partner', string='Cliente', compute='_compute_client_id', store=True)
    folio_pedido = fields.Char('Folio del pedido', readonly=True, copy=False, compute='_compute_folio_pedido', store=True)

    @api.depends('production_id.client_id')
    def _compute_client_id(self):
        for workorder in self:
            workorder.client_id = workorder.production_id.client_id

    @api.depends('production_id.folio_pedido')
    def _compute_folio_pedido(self):
        for workorder in self:
            workorder.folio_pedido = workorder.production_id.folio_pedido
