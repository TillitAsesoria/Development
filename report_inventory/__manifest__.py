# -*- coding: utf-8 -*-
{
    'name': "Reporte de Inventario",

    'summary': """
        Presentar una vista en la que se muestre un listado de productos, así como su existencia, su costo unitario y valor del total por ubicación, así como el tiempo que lleva en cada ubicación, ya sea por adquisición o por transferencia. """,

    'description': """
        Presentar una vista en la que se muestre un listado de productos, así como su existencia, su costo unitario y valor del total por ubicación, así como el tiempo que lleva en cada ubicación, ya sea por adquisición o por transferencia.
    """,

    'author': "Yeniel Leon Ferre",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_enterprise','stock','stock_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_inventory_tree.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
