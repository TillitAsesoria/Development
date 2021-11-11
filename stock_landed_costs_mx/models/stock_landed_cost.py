# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLandedCostInherit(models.Model):
    _inherit = 'stock.landed.cost'

    type_selection = fields.Selection([('gec', 'Gasto de envío común'), ('p', 'Pedimento')], string='Tipo de Costo', default='gec')

    @api.constrains('l10n_mx_edi_customs_number')
    def _check_l10n_mx_edi_customs_number(self):
        for landed_cost in self:
            if landed_cost.l10n_mx_edi_customs_number:
                return super(StockLandedCostInherit, self)._check_l10n_mx_edi_customs_number()