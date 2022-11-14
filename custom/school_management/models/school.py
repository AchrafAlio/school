# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SchoolClass(models.Model):
    _name = "school.class"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Class"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Class Sequence', copy=False, readonly=True, required=True,
                           default=lambda self: _('New'))
    capacity = fields.Integer(string='Capacity')
    total_students = fields.Integer(string='Total Students', compute="_total_students")
    remaining_seats = fields.Integer(string='Remaining Seats', compute="_remaining_seats")
    color = fields.Char(string='Color')

    standard_id = fields.Many2one(comodel_name='school.standard', string="Standard")
    teacher_id = fields.Many2one(comodel_name='school.teacher', string="Teacher")
    classroom_id = fields.Many2one(comodel_name='school.classroom', string="Room Number")

    # student_ids = fields.Many2many(comodel_name='school.student', string="Students")

    student_ids = fields.One2many(comodel_name='school.student', inverse_name='class_id',
                                  string='Class students', store=True)
    subject_ids = fields.One2many(comodel_name='school.subject', inverse_name='class_id', string="Subjects")

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.class') or _('New')
        res = super(SchoolClass, self).create(vals)
        print("vals ============> ", vals['sequence'])
        print("res =============> ", vals['student_ids'])
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


class SchoolMedium(models.Model):
    _name = "school.medium"
    _description = "School Medium"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Sequence')
    code = fields.Char(string='Code')
    description = fields.Char(string='Description')


class SchoolDivision(models.Model):
    _name = "school.division"
    _description = "School Division"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Sequence')
    code = fields.Char(string='Code')
    description = fields.Char(string='Description')


class SchoolClassroom(models.Model):
    _name = "school.classroom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Classroom"

    name = fields.Char(string='Name', required=True)
    room_number = fields.Char(string='Room Number')


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
