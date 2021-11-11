import base64
from xml.dom import minidom

from odoo import fields, models, api


class ImportXmlSat(models.Model):
    _name = 'import.xml.sat'
    _description = 'Description'
    _rec_name = 'name'

    @api.depends('doc_xml')
    def _compute_full_name(self):
        self.ensure_one()
        if self.doc_xml:
            docxml = base64.decodebytes(self.doc_xml)
            doc = minidom.parseString(docxml)
            timbre = doc.getElementsByTagName("tfd:TimbreFiscalDigital")
            for tin in timbre:
                self.name = tin.getAttribute('UUID')
                print('name', self.name)


    name = fields.Char('UUID', compute=_compute_full_name)
    doc_xml = fields.Binary('XML', attachment=False, copy=True)





class AccountMove(models.Model):
    _inherit = 'account.move'

l10n_mx_edi_cfdi_uuid = fields.Char(string='Fiscal Folio', copy=True, readonly=False,
        help='Folio in electronic invoice, is returned by SAT when send to stamp.',
        compute='_compute_cfdi_values')