from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo import api, fields, models

class SchoolSession(models.Model):
    _name = 'school.session'
    _description = 'School Session System'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(string='Duration', digits=(6,2))
    seats = fields.Integer(string='Seats')
    course_id = fields.Many2one('school.course', string='Course', required=True)
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    attendance_id = fields.Many2many('res.partner', string='Attendance')
    taken_seats = fields.Float(string='Taken Seats', compute='_taken_seats')
    end_date = fields.Date(string='End Date', store=True, compute='_get_end_date', inverse='_set_end_date')
    attendace_count = fields.Integer(string='Attendace Count', compute='_get_attendance_count', store=True)
    color = fields.Integer()


    @api.depends('seats','attendance_id')
    def _taken_seats(self):
        for r in self:
            if r.seats > 0:
                r.taken_seats = 100 * len('attendance_id') / r.seats
            else:
                r.taken_seats = 0.0

    @api.depends('attendance_id')
    def _get_attendance_count(self):
        for r in self:
            r.attendace_count = len(r.attendance_id)


    @api.onchange('seats','attendance_id')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                    'title': "Incorrect 'seats' values",
                    'message': "The number of available seats say not be negative",
                },
            }

        if self.seats < len(self.attendance_id):
            return {
                'warning':{
                    'title': 'Too many attendances',
                    'message': 'Increase seats or remove excess attendances'
                },
            }

    @api.constrains('instructor_id','attendance_id')
    def _check_instructor_not_in_attendance(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendance_id:
                raise ValidationError("A session's instructor can't be an attendee")


    @api.depends('start_date','duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration


    def _set_end_date(self):
        for r in self:
            if not(r.start_date and r.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days+1

