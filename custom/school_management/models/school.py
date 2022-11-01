# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolClass(models.Model):
    _name = "school.class"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Class"

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    total_students = fields.Integer(string='Total Students', compute="_total_students")
    remaining_seats = fields.Integer(string='Remaining Seats', compute="_remaining_seats")
    color = fields.Char(string='Color')
    standard_id = fields.Many2one(comodel_name='school.standard', string="Standard")
    teacher_id = fields.Many2one(comodel_name='school.teacher', string="Teacher")
    classroom_id = fields.Many2one(comodel_name='school.classroom', string="Room Number")

    student_ids = fields.One2many(comodel_name='school.student', inverse_name='class_id', string="Students" )
    subject_ids = fields.One2many(comodel_name='school.subject', inverse_name='class_id', string="Subjects")

    def _remaining_seats(self):
        for rec in self:
            rec.remaining_seats = rec.capacity - rec.total_students

    @api.onchange('student_ids')
    def _total_students(self):
        for rec in self:
            rec.total_students += 1
            print(rec.student_ids)

class SchoolStandard(models.Model):
    _name = "school.standard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
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


class SchoolSubject(models.Model):
    _name = "school.subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Subject"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    standard_ids = fields.One2many(comodel_name='school.standard', inverse_name='subject_id', string="Standards")
    teacher_ids = fields.One2many(comodel_name='school.teacher', inverse_name='subject_id', string="Teachers")
    student_id = fields.Many2one(comodel_name='school.student', string='Student')
    class_id = fields.Many2one(comodel_name='school.class', string='Class')
