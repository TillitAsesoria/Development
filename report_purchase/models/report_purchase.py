# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ReportPurchase(models.Model):
    _inherit = 'purchase.report'
    _description = 'Reporte de Compra Tree'

    @api.model
    def _total_venta(self):
        for to in self:
            to.total_venta = to.qty_ordered * to.standard_price

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
            profile = factu[0].name.split("/")
            name = profile[3]
            if name:
                pymen = self.env['account.payment'].search([('ref', '=', name)])
                fact.payment_reference = pymen.name
                return fact.payment_reference


    @api.model
    def _cumpute_coste(self):
        for pro in self.product_id:
            cant = 0
            precio = 0
            coste = self.env['purchase.order.line'].search([('product_id', '=', int(pro.id))])
            for cos in coste:
               cant = cant + (cos.product_qty * cos.price_unit)
               precio = precio + cos.price_unit
            result = cant / precio
            self.costo_promedio = result

    standard_price = fields.Float(related='product_id.standard_price', string='Costo')
    total_venta = fields.Float(string='Total Venta', compute=_total_venta)
    costo_promedio = fields.Float(string='Costo Promedio Nuevo *', compute=_cumpute_coste)
    albaran = fields.Char(string='Albarán', compute=_cumpute_albaran)
    move_name = fields.Char(string='Factura', compute=_cumpute_fatura)
    payment_reference = fields.Char(string='Pago', compute=_cumpute_payment)