from datetime import datetime
from xml.dom import minidom
import base64
import xml.etree.ElementTree as ET
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class ImportXmlInvoiceWizard(models.Model):
    _name = 'import.xml.invoice.wizard'
    _description = 'Description'

    # xml_doc = fields.Many2many('import.xml.sat', 'sat_wizard_id', 'sat_id', string='Documento XML')
    xml_ids = fields.Many2many('ir.attachment',string='XML')

    def existe_factura(self, cant, date):
        existe = self.env['account.move'].search([('amount_untaxed', '=', round(cant,2))])
        if existe and str(existe.invoice_date) == date:
            return True
        return False

    def import_xml(self):
        self.ensure_one()
        for imp in self.xml_ids:
            cont = imp.name
            store = imp.store_fname
            size = imp.file_size
            datas = imp.db_datas
            print('IDS', cont)
            print('store', store)
            print('data', imp.datas)
            docxml = base64.decodebytes(imp.datas)
            doc = minidom.parseString(docxml)
            comprobante = doc.getElementsByTagName("cfdi:Comprobante")
            nota = doc.getElementsByTagName("cfdi:CfdiRelacionados")
            emisor = doc.getElementsByTagName("cfdi:Emisor")
            receptor = doc.getElementsByTagName("cfdi:Receptor")
            conceptos = doc.getElementsByTagName("cfdi:Concepto")
            complemento = doc.getElementsByTagName("cfdi:Complemento")
            impusto = doc.getElementsByTagName("cfdi:Traslado")
            timbre = doc.getElementsByTagName("tfd:TimbreFiscalDigital")
            nota_credito = ''
            for n in nota:
                nota_credito = n.getAttribute('TipoRelacion')
            for com in comprobante:
                metedopago = com.getAttribute("MetodoPago")
                condiciones = com.getAttribute("CondicionesDePago")

            client = []
            for em in emisor:
                rfc = em.getAttribute("Rfc")
                nombre = em.getAttribute("Nombre")
                regimenFiscal = em.getAttribute("RegimenFiscal")
                if rfc == 'XEXX010101000':
                    client = self.env['res.partner'].search([('name', '=', str(nombre))])
                elif rfc == 'XAXX010101000':
                    client = self.env['res.partner'].search([('name', '=', str(nombre))])

                client = self.env['res.partner'].search([('vat', '=', str(rfc))])
                if not client:
                    clientes = self.env['res.partner'].create({
                        'name': nombre,
                        'vat': rfc
                    })
            company = []
            for re in receptor:
                nombrerec = re.getAttribute("Nombre")
                rfcrec = re.getAttribute("Rfc")
                usoccdi = re.getAttribute("UsoCFDI")
                if rfcrec == 'XEXX010101000':
                    company = self.env['res.partner'].search([('name', '=', str(nombrerec))])
                elif rfcrec == 'XAXX010101000':
                    company = self.env['res.partner'].search([('name', '=', str(nombrerec))])

                company = self.env['res.partner'].search([('vat', '=', str(rfcrec))])
                if not company:
                    compania = self.env['res.partner'].create({
                        'name': nombrerec,
                        'vat': rfcrec
                    })

            for imp in impusto:
                amount = float(imp.getAttribute("TasaOCuota")) * 100
                if client.vat == 'GAU101208N69':
                    tax_id = self.env['account.tax.template'].search(
                        [('amount', '=', int(amount)),
                         ('name', '=', ('IVA(16%) VENTAS', 'IVA(0%) VENTAS', 'IVA(8%) VENTAS'))])
                else:
                    tax_id = self.env['account.tax.template'].search(
                        [('amount', '=', int(amount)), ('name', 'in', (
                        'IVA(16%) COMPRAS', 'IVA(8%) COMPRAS', 'RET IVA FLETES 4%', 'RET IVA ARRENDAMIENTO 10%',
                        'RET ISR ARRENDAMIENTO 10%', 'RET ISR HONORARIOS 10%', 'RETENCION IVA ARRENDAMIENTO 10.67%',
                        'RETENCION IVA HONORARIOS 10.67%', 'IVA(0%) COMPRAS'))])

            payment_pago_term = self.env['account.payment.term'].search([('name', '=', str(condiciones))])
            cant = 0.00
            move_line = []
            for pro in conceptos:
                claveProdServ = pro.getAttribute('ClaveProdServ')
                identification = pro.getAttribute('NoIdentificacion')
                cantidad = pro.getAttribute('Cantidad')
                claveUnidad = pro.getAttribute('ClaveUnidad')
                unidad = pro.getAttribute('Unidad')
                descripcion = pro.getAttribute('Descripcion')
                cant = cant + float(pro.getAttribute('ValorUnitario'))
                valorUnitario = pro.getAttribute('ValorUnitario')
                importe = pro.getAttribute('Importe')
                unspsc_product = self.env['product.unspsc.code'].search([('code', '=', str(claveProdServ))])
                print('Valor', unspsc_product.name)
                print('Valor1', claveProdServ)
                if identification:
                    product = self.env['product.template'].search([('unspsc_code_id', '=', int(unspsc_product.id)), ('default_code', '=', str(identification))])
                else:
                    product = self.env['product.template'].search([('name', '=', str(descripcion))])
                if not product:
                    producto = self.env['product.template'].create({
                        'name': descripcion,
                        'unspsc_code_id': unspsc_product.id,
                        'default_code': identification or ''
                    })
                    move_line.append({
                        'product_id': producto.id,
                        'quantity': cantidad,
                        'price_unit': valorUnitario,
                        'price_subtotal': importe,
                        'tax_ids': tax_id
                    })

                else:
                    move_line.append({
                        'product_id': product.id,
                        'quantity': cantidad,
                        'price_unit': valorUnitario,
                        'price_subtotal': importe,
                        'tax_ids': tax_id
                    })


            for tim in timbre:
                fecha = tim.getAttribute('FechaTimbrado')
                timbre_digital = tim.getAttribute('UUID')
                fechastr = fecha.split("-")
                dia = fechastr[2][0:2]
                mes = fechastr[1]
                anno = fechastr[0]
                hora = fechastr[2][3:5]
                horar = fechastr[2].split(":")
                minutos = horar[1]
                segundos = horar[2]
                fechastring = dia + '/' + mes + '/' + anno + ' ' + hora + ':' + minutos + ':' + segundos
                fechafact = datetime.strptime(fechastring, '%d/%m/%Y %H:%M:%S')
                date_invoice = str(fechafact.date())
                print('Fecha', fechafact.date())
            if not self.existe_factura(cant, date_invoice):
                if nota_credito:
                    if client.vat == 'GAU101208N69':
                        invoice = self.env['account.move'].create({
                            'partner_id': company.id if company else compania.id,
                            'move_type': 'out_refund',
                            'invoice_date': fechafact.date(),
                            'l10n_mx_edi_payment_policy': metedopago,
                            'l10n_mx_edi_cfdi_uuid': timbre_digital,
                            'invoice_payment_term_id': payment_pago_term.id if condiciones != '' else payment_pago_term,
                            'invoice_line_ids': move_line

                        })
                        self.env['ir.attachment'].create({
                            'res_model': 'account.move',
                            'name': cont,
                            'res_id': invoice.id,
                            'type': 'binary',
                            'company_id': client.id if client else clientes.id,
                            'store_fname': store,
                            'file_size': size,
                            'db_datas': datas
                        })
                    if company.vat == 'GAU101208N69':
                        invoice = self.env['account.move'].create({
                            'partner_id': client.id if client else clientes.id,
                            'move_type': 'in_refund',
                            'invoice_date': fechafact.date(),
                            'l10n_mx_edi_payment_policy': metedopago,
                            'l10n_mx_edi_cfdi_uuid': timbre_digital,
                            'invoice_payment_term_id': payment_pago_term.id if condiciones != '' else payment_pago_term,
                            'invoice_line_ids': move_line
                        })
                        self.env['ir.attachment'].create({
                            'res_model': 'account.move',
                            'name': cont,
                            'res_id': invoice.id,
                            'type': 'binary',
                            'company_id': company.id if company else compania.id,
                            'store_fname': store,
                            'file_size': size,
                            'db_datas': datas
                        })
                else:
                    if client.vat == 'GAU101208N69':
                        invoice = self.env['account.move'].create({
                            'partner_id': company.id if company else compania.id,
                            'move_type': 'out_invoice',
                            'invoice_date': fechafact.date(),
                            'l10n_mx_edi_payment_policy': metedopago,
                            'l10n_mx_edi_cfdi_uuid': timbre_digital,
                            'invoice_payment_term_id': payment_pago_term.id if condiciones != '' else payment_pago_term,
                            'invoice_line_ids': move_line
                        })
                        self.env['ir.attachment'].create({
                            'res_model': 'account.move',
                            'name': cont,
                            'res_id': invoice.id,
                            'type': 'binary',
                            'company_id': client.id if client else clientes.id,
                            'store_fname': store,
                            'file_size': size,
                            'db_datas': datas
                        })
                    if company.vat == 'GAU101208N69':
                        invoice = self.env['account.move'].create({
                            'partner_id': client.id if client else clientes.id,
                            'move_type': 'in_invoice',
                            'invoice_date': fechafact.date(),
                            'l10n_mx_edi_payment_policy': metedopago,
                            'l10n_mx_edi_cfdi_uuid': timbre_digital,
                            'invoice_payment_term_id': payment_pago_term.id if condiciones != '' else payment_pago_term,
                            'invoice_line_ids': move_line
                        })
                        self.env['ir.attachment'].create({
                            'res_model': 'account.move',
                            'name': cont,
                            'res_id': invoice.id,
                            'type': 'binary',
                            'company_id': company.id if company else compania.id,
                            'store_fname': store,
                            'file_size': size,
                            'db_datas': datas
                        })
