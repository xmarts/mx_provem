# -*- coding: utf-8 -*-
{
    'name': "Provem Buttons",

    'summary': """
       Personalizaciones""",

    'description': """
   Personalizaciones
    """,

    'author': "Nayeli Valencia Díaz",
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/sales_team_security.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}