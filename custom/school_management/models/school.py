# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class SchoolClass(models.Model):
    _name = "school.class"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Class"
    _rec_name = "sequence"

    sequence = fields.Char(string='Class Sequence', copy=False, compute="_name_compose", readonly=True,
                           default=lambda self: _('New'))
    capacity = fields.Integer(string='Capacity')
    total_students = fields.Integer(string='Total Students', compute="_total_students")
    remaining_seats = fields.Integer(string='Remaining Seats', compute="_remaining_seats")
    division = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C')], default='A')
    medium = fields.Selection([('arabic', 'Arabic'), ('english', 'English'), ('french', 'French'),
                               ('urdu', 'Urdu')], default='arabic')
    color = fields.Char(string='Color')
    standard_id = fields.Many2one(comodel_name='school.standard', string="Standard")
    standard_name = fields.Char(related="standard_id.name", store=True)

    classroom_id = fields.Many2one(comodel_name='school.classroom', string="Room Number")
    student_ids = fields.One2many(comodel_name='school.student', inverse_name='class_id',
                                  string='Class students', store=True)
    teacher_ids = fields.Many2many(comodel_name='school.teacher', string="Teachers")
    # , compute="_sujects_teachers")
    subject_ids = fields.Many2many(comodel_name='school.subject', string="Subjects",
                                   )
    user_id = fields.Many2one(comodel_name="res.users", string='User ID', default=lambda self: self._context.get('uid'),
                              store=False)
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    def _name_compose(self):
        for rec in self:
            rec.sequence = str(rec.standard_id.name) + "[" + rec.division + "]"

    @api.onchange('sequence')
    def _check_sequence(self):
        print(self.sequence)
        for record in self:
            print(record.sequence)

    _sql_constraints = [
        ('unique_standard_division_class', 'unique (standard_id,division)', 'This class has already been created'),
        ('unique_class_room', 'unique (classroom_id)', 'This class room has already been occupied')
    ]

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.sequence
            # self.env['ir.sequence'].next_by_code('school.class') or _('New')
        res = super(SchoolClass, self).create(vals)

        return res

    def _remaining_seats(self):
        for rec in self:
            rec.remaining_seats = rec.capacity - rec.total_students

    @api.onchange('student_ids')
    def _total_students(self):
        for rec in self:
            rec.total_students = 0
            for student in rec.student_ids:
                rec.total_students += 1

    def _sujects_teachers(self):
        for subject in self.subject_ids:
            print(subject, subject.teacher_ids)
            self.teacher_ids += subject.teacher_ids


class SchoolStandard(models.Model):
    _name = "school.standard"
    _description = "School Standard"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Sequence')
    code = fields.Char(string='Code')
    description = fields.Char(string='Description')
    subject_id = fields.Many2one('school.subject', string='Subject')


class SchoolClassroom(models.Model):
    _name = "school.classroom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Classroom"

    name = fields.Char(string='Name', required=True)
    room_number = fields.Char(string='Room Number')

    # _sql_constraints = [
    #     ('unique_class_room', 'unique (name)', 'This class room has already been occupied')
    # ]


class SchoolSubject(models.Model):
    _name = "school.subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Subject"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    standard_ids = fields.One2many(comodel_name='school.standard', inverse_name='subject_id', string="Standards")
    teacher_ids = fields.One2many(comodel_name='school.teacher', inverse_name='subject_id', string="Teachers")
    student_id = fields.Many2one(comodel_name='school.student', string='Student')
    class_id = fields.Many2one('school.class')


class SchoolReminder(models.Model):
    _name = "school.reminder"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Reminder"

    def get_user_name(self):
        # find the user with the current user id
        user = self.env['res.users'].browse(self._context.get('uid'))
        # get the record for the user in res.users to have login(name) and id
        record = self.env["res.users"].search([('id', '=', user.id)])
        return record.login

    def get_student_user_id(self):
        for rec in self:
            rec.student_user_id = rec.env['school.student'].browse(rec.student_id).id.user_id.id

    # the name of the user who creates the notification activity
    name = fields.Char(string='Name', default=get_user_name, required=True, readonly=True)
    # the id of the user who creates the notification activity
    user_id = fields.Many2one(comodel_name='res.users', string='Current uid',
                              default=lambda self: self._context.get('uid'), readonly=True)
    class_id = fields.Many2one(comodel_name="school.class", string="Class")
    student_id = fields.Many2one(comodel_name='school.student', string='Student', required=True,
                                 domain="[('class_id','=', class_id)]")
    student_user_id = fields.Char(string="Student user id", compute="get_student_user_id")
    message = fields.Char(string="Message", required=True)

    def action_send_notification(self):
        student = self.env['school.student'].browse(self.student_id)
        print(student.id.user_id)
        print(student.id.user_id.id)
        self.activity_schedule('school_management.mail_notify_student', date_deadline=date.today(),
                               user_id=student.id.user_id.id, note='Notification from teacher')
