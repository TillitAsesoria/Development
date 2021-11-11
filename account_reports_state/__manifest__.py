# -*- coding: utf-8 -*-
{
    'name': "Estados de Cuenta",

    'summary': """
        Estados de cuentas por pagar y por cobrar""",

    'description': """
       Estados de cuentas por pagar y por cobrar
    """,

    'author': "Yeniel Leon Ferre",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_reports','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_state_client.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
