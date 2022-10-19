# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '1.0',
    'sequence': -100,
    'description': """Hospital Management Software""",
    'category': 'Productivity/Discuss',
    'website': 'https://www.softifi.com',
    'license': 'LGPL-3',
    'depends': [ 'base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'views/sale.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}