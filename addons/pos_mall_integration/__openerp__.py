# -*- coding: utf-8 -*-
{
    'name': "pos_mall_integration",

    'summary': """
        Function to generate end of day file, for Asiamall integration by ftp
        """,

    'description': """
        Function to generate end of day file, for Asiamall integration by ftp
        by calculating total sales and no of receipts

        Configuration available:

        tenant-id
        ftp address & password

    """,

    'author': "Technecraft, Deddy",
    'website': "http://www.technecraft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '3.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'res_config_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}