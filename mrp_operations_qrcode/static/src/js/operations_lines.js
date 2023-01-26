odoo.define('mrp_operations_qrcode.OperationsLines', function (require) {
'use strict';

var concurrency = require('web.concurrency');
var core = require('web.core');
var Widget = require('web.Widget');

var OperationsLine = require('mrp_operations_qrcode.OperationsLine');


var OperationsLines = Widget.extend({
    template: 'operations_lines',

    init: function (parent) {
        this._super.apply(this, arguments);

        this.lines = [];
        this.mutex = new concurrency.Mutex();
        this.workorder_states;
        this.today_orders;
    },

    willStart: function () {
        return Promise.all([
            this._super.apply(this, arguments),
            this._get_workorder_states(),
            this._get_today_orders()
        ]);
    },

    start: function () {
        var self = this;

        return this._super.apply(this, arguments).then(function () {
            core.bus.on('barcode_scanned', self, self._on_barcode_scanned_handler);
            self.show_today_orders();
        });
    },

    destroy: function () {
        core.bus.off('barcode_scanned', this, this._on_barcode_scanned_handler);
        this._super();
    },

    _get_workorder_states: function () {
        var self = this;

        return this._rpc({
            model: 'mrp.workorder',
            method: 'get_states_selection',
            args: [[]]
        }).then(function (states) {
            self.workorder_states = states;
        });
    },

    _on_barcode_scanned_handler: function (barcode) {
        var self = this;

        this.mutex.exec(function () {
            return self._on_barcode_scanned(barcode);
        });
    },

    _on_barcode_scanned: async function (barcode) {
        var self = this;

        var splitted_barcode = barcode.split(',');

        if (splitted_barcode.length !== 2) {
            this.displayNotification({
                type: 'danger',
                message: 'El formato del código QR no es válido'
            });

            return;
        }

        var order_id = parseInt(splitted_barcode[1]);

        if (!this._order_exists(order_id)) {
            this.displayNotification({
                type: 'warning',
                message: 'No se encontró la orden escaneada'
            });

            return;
        }

        var line_index = this._get_line_index(order_id);
        var is_new_line = (line_index === false) ? true : false;
        var line = (line_index !== false) ? this.lines[line_index] : null;

        this._operations_next_stage(order_id).then(function (status) {
            if (status === 'danger') {
                return;
            }
            if (is_new_line) {
                self.add_line(order_id, 'fade_in');
            } else {
                if (status !== 'warning') {
                    self.update_line(line, line_index);
                }
            }
        });
    },

    add_line: function (order_id, animation_type) {
        var line = new OperationsLine(this, order_id, animation_type);
        var body = this.$el.find('.qr_lines');
        this.lines.unshift(line);
        line.prependTo(body);
    },

    update_line: async function (line, line_index) {
        // Si la línea resulta ser la primera, solo se actualizará su información
        if (line_index === 0) {
            line.update_data(line.order_id);
        } else {
            // Si no es la primer línea, se eliminará para volver a insertarla
            // como primer línea
            await line.take_out();
            this.lines.splice(line_index, 1);
            this.add_line(line.order_id, 'slide_up');
            line.destroy();
        }
    },

    _operations_next_stage: function (order_id) {
        var self = this;

        return this._rpc({
            model: 'mrp.production',
            method: 'operations_next_stage',
            args: [order_id]
        }).then(function(result) {
            self.displayNotification({
                type: result.status,
                title: result.order,
                message: result.message
            });

            return result.status;
        });
    },

    _order_exists: function (order_id) {
        return this._rpc({
            model: 'mrp.production',
            method: 'search',
            args: [[['id', '=', order_id]]]
        }).then(function (order) {
            if (order.length != 0) {
                return true;
            } else {
                return false;
            }
        });
    },

    _get_line_index: function (order_id) {
        for (let i = 0; i < this.lines.length; i++) {
            if (this.lines[i].order_id == order_id) {
                return i;
            }
        }

        return false;
    },

    _get_today_orders: function () {
        var self = this;

        return this._rpc({
            model: 'mrp.production',
            method: 'today_orders',
            args: [[]]
        }).then(function (orders) {
            self.today_orders = orders;
        });
    },

    show_today_orders: function () {
        var self = this;

        this.today_orders.forEach(function (order) {
            self.add_line(order.id, 'fade_in');
        });
    }
});


return OperationsLines;

});
