{
    'name': 'Rakib Academy',
    'version': '1.0',
    'category': 'Education',
    'summary': 'A module to manage Rakib Academy operations',
    'description': 'This module allows you to manage students, courses, and enrollments at Rakib Academy.',
    'author': 'Rakib',
    'depends': ['base'],  # Add any other dependencies here
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/school_course.xml',
        'views/school_session.xml',
    ],
    'demo': [
        'demo/demo.xml',  # Add demo data if any
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
