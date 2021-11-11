# -*- coding: utf-8 -*-
{
    'name': "Stock Landed Cost MX",

    'summary': """
        Agregando campos para ocultar otro""",

    'description': """
        Modificando la clase stock landed cost
    """,

    'author': "Yeniel Leon Ferre",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_landed_costs','l10n_mx_edi_landing'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_landed_cost_inherit.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
