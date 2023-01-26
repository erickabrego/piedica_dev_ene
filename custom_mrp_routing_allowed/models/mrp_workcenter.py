# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MRPWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    x_allowed_user_ids = fields.Many2many(comodel_name="res.users", string="Usuarios permitidos")

    def is_user_allowed(self, user_id):
        self.ensure_one()

        return user_id in self.x_allowed_user_ids.mapped('id')
