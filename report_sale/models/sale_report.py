# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReportSale(models.Model):
    _inherit = 'sale.report'
    _description = 'Reporte de Venta'

    @api.model
    def _total_coste(self):
        for to in self:
            to.total_coste = to.product_uom_qty * to.standard_price

    @api.model
    def _total_venta(self):
        for to in self:
            to.total_venta = to.product_uom_qty * to.price

    @api.model
    def _calcular_utilidad(self):
        for to in self:
            to.utilidad = to.total_venta - to.total_coste

    @api.model
    def _calcular_margen(self):
        for to in self:
            result = to.utilidad / to.total_venta * 100
            to.margen= str(round(result, 2)) + '%'

    @api.model
    def _cumpute_albaran(self):
        origenes = self.env['stock.picking'].search([])
        for al in self:
            for ori in origenes:
                if ori.origin == al.order_id.name:
                    al.albaran = ori.name

    @api.model
    def _cumpute_fatura(self):
        for fact in self:
            factu = self.env['account.move'].search([('invoice_origin', '=', fact.order_id.name)])
            if factu:
                fact.move_name = factu.name

    @api.model
    def _cumpute_payment(self):
        for fact in self:
            factu = self.env['account.move'].search([('invoice_origin', '=', fact.order_id.name)])
            pymen = self.env['account.payment'].search([('ref', '=', factu.name)])
            if pymen:
                fact.payment_reference = pymen.name

    standard_price = fields.Float(related='product_id.standard_price', string='Costo')
    price = fields.Float(related='product_id.list_price', string='Precio')
    total_coste = fields.Float(string='Total Costo', compute=_total_coste)
    total_venta = fields.Float(string='Total Venta', compute=_total_venta)
    utilidad = fields.Float('Utilidad', compute=_calcular_utilidad)
    margen = fields.Char('Margen de Utilidad', compute=_calcular_margen)
    albaran = fields.Char(string='Albarán', compute=_cumpute_albaran)
    move_name = fields.Char(string='Factura', compute=_cumpute_fatura)
    payment_reference = fields.Char(string='Pago', compute=_cumpute_payment)