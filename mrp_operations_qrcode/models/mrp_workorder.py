from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    operate_date = fields.Datetime()
    in_rollback = fields.Boolean(default=False)

    def button_start(self):
        res = super().button_start()

        self.production_id.update_operation_index(self.id)
        end_date = datetime.now()
        self.write({'operate_date': end_date})
        self.production_id.write({'operate_date': end_date})

        return res

    def button_finish(self):
        res = super().button_finish()

        end_date = datetime.now()

        for workorder in self:
            workorder.write({'operate_date': end_date})
            workorder.production_id.write({'operate_date': end_date})

            if workorder.in_rollback:
                workorder.write({'in_rollback': False})

        return res

    def button_pending(self):
        res = super().button_pending()

        end_date = datetime.now()

        for workorder in self:
            workorder.write({'operate_date': end_date})
            workorder.production_id.write({'operate_date': end_date})

        return res

    def button_go_back(self):
        """
        Vuelve a poner en estado "preparado" la operación ya terminada, para que
        la siguiente vez que se escanee la orden esta operación sea la que se
        lleve a cabo
        """

        self.ensure_one()

        next_order = self.next_work_order_id

        if next_order and (next_order.state == 'ready' or next_order.state == 'progress'):
            next_order.write({'state': 'pending'})

        self.write({
            'state': 'ready',
            'in_rollback': True
        })

    def _calculate_duration_expected(self, date_planned_start=False, date_planned_finished=False):
        """
        La duración esperada debe mantenerse como está definida originalmente en
        las operaciones, no recalcularse cada vez que se "reinicia" la operación,
        ya que si el tiempo esperado es enorme eso impediría poder terminar
        la operación cuando se escanea
        """

        return self.duration_expected

    def try_to_finish_from_scan(self):
        """
        Se usa principalmente para poder hacer la validación de que haya pasado
        el tiempo mínimo requerido para poder finalizar la operación mediante
        el escaneo de QR
        """

        # Permite al usuario finalizar la operación antes del tiempo mínimo en
        # el caso de que la operación sea un ajuste y no una operación normal
        if (self.in_rollback):
            return self.button_finish()

        res = self.env['mrp.workcenter.productivity'].search([('workorder_id', '=', self.id), ('date_end', '=', False)])

        if not res:
            return {
                'status': 'warning',
                'message': ('Hubo un problema con la operación <b>%s</b>' % self.name)
            }

        date_start = res[0].date_start
        diff = datetime.now() - date_start
        duration = diff.seconds
        minutes = int(duration / 60) >> 0;
        seconds = duration % 60;
        duration_float = minutes + seconds / 60;

        if duration_float < self.duration_expected:
            return {
                'status': 'warning',
                'message': ('Aun no ha pasado el tiempo mínimo para terminar la operacion <b>%s</b>' % self.name)
            }

        return self.button_finish()

    def get_states_selection(self):
        return dict(self._fields['state']._description_selection(self.env))
