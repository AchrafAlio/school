# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
    teacher_id = fields.Many2one(comodel_name='school.teacher', string="Teacher")
    classroom_id = fields.Many2one(comodel_name='school.classroom', string="Room Number")

    student_ids = fields.One2many(comodel_name='school.student', inverse_name='class_id',
                                  string='Class students', store=True)
    subject_ids = fields.Many2many(comodel_name='school.subject', string="Subjects")

    def _name_compose(self):
        for rec in self:
            rec.sequence = str(rec.standard_id.name) + "[" + rec.division + "]"

    @api.onchange('sequence')
    def _check_sequence(self):
        print(self.sequence)
        for record in self:
            print(record.sequence)
            # if record.date_end < fields.Date.today():
            #     raise ValidationError("The end date cannot be set in the past")
        # all records passed the test, don't return anything

    # @api.onchange('sequence')
    # def loop(self):
    #     if self.sequence:
    #         for rec in self:
    #                if self.sequence == rec.sequence:
    #                    raise ValidationError("This class has already been created")

    _sql_constraints = [
        ('unique_standard_division_class', 'unique (standard_id,division)', 'This class has already been created'),
        ('unique_class_room', 'unique (classroom_id)', 'This class room has already been occupied')
    ]

    @api.model
    def create(self, vals):
        print("vals ============> ", vals)
        print("self.env ============> ", self.env)
        print("division =============> ", vals['division'])
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
        print("student_ids changed!!!!!!!!!!!!!!!!")
        for rec in self:
            rec.total_students = 0
            for student in rec.student_ids:
                rec.total_students += 1


class SchoolStandard(models.Model):
    _name = "school.standard"
    _description = "School Standard"

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
