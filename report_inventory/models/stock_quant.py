# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _calcular_antiguedad(self):
        days = datetime.now()
        for ant in self:
            if ant.in_date:
                result = days - ant.in_date
                ant.antiguedad = str(result.days) + ' Días'

    @api.model
    def _compute_coste(self):
        for pro in self.product_id:
            if pro:
                self.coste = pro.standard_price

    coste = fields.Float(string='Coste', compute=_compute_coste)
    antiguedad = fields.Char(string='Antigüedad', compute=_calcular_antiguedad)


    @api.model
    def _get_quants_action_tree(self, domain=None, extend=False):#
        """ Returns an action to open quant view.
        Depending of the context (user have right to be inventory mode or not),
        the list view will be editable or readonly.

        :param domain: List for the domain, empty by default.
        :param extend: If True, enables form, graph and pivot views. False by default.
        """
        self._quant_tasks()
        ctx = dict(self.env.context or {})
        ctx.pop('group_by', None)
        action = {
            'name': _('Stock Inventory'),
            'view_type': 'tree',
            'view_mode': 'list',
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'domain': domain or [],
            'help': """
                    <p class="o_view_nocontent_empty_folder">No Stock On Hand</p>
                    <p>This analysis gives you an overview of the current stock
                    level of your products.</p>
                    """
        }

        if self._is_inventory_mode():
            action['view_id'] = self.env.ref('report_inventory.view_stock_quant_tree_inventory').id
        action.update({
            'views': [
                (action['view_id'], 'list'),
            ],
        })
        return action

    @api.model
    def action_view_quants_tree(self):
        if self.user_has_groups('stock.group_stock_manager'):
            self = self.with_context(inventory_mode=True)
        return self._get_quants_action_tree(extend=False)
