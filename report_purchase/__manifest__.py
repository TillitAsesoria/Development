# -*- coding: utf-8 -*-
{
    'name': "Reporte de Compra",

    'summary': """
       Reporte de Compra""",

    'description': """
        Reporte de Compra
    """,

    'author': "Yeniel Leon Ferre",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'purchase_stock', 'purchase_stock_enterprise','purchase_enterprise'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_purchase_tree_view.xml'
    ],

}
