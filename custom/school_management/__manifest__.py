# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'version': '1.0',
    'sequence': -100,
    'description': """School Management Software""",
    'category': 'Productivity/Discuss',
    'website': 'https://www.softifi.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail','hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/res_config_settings_views.xml',
        'views/class_view.xml',
        'views/standard_view.xml',
        'views/classroom_view.xml',
        'views/subject_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'report/student_card.xml',
        'report/student_details_template.xml',
        'report/report.xml',
        'views/menu.xml',


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
