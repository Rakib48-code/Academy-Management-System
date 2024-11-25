from odoo import api, fields, models

class SchoolCourse(models.Model):
    _name = 'school.course'
    _description = 'School Course System'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    session_id = fields.One2many('school.session', 'course_id', string='Sessions')

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]