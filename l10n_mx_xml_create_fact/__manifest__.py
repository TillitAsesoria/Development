# -*- coding: utf-8 -*-
{
    'name': "Import información del SAT",

    'summary': """
        Importar xml del sat""",

    'description': """
        Crear la factura que depende de un xml sel sat
    """,

    'author': "Yeniel leon ferre",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','l10n_mx_edi_extended'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/import_xml_sat.xml',
        'wizard/import_xml_invoice_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
