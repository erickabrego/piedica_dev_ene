from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    x_commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Entidad")