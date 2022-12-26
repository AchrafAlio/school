# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Teacher"

    name = fields.Char(string='Teacher Name', required=True)
    email = fields.Char(string='Teacher email', required=True)
    picture = fields.Binary(string='Picture')
    subject_id = fields.Many2one(comodel_name='school.subject', string='Subject')
    school_name = fields.Char(string="School Name",
                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                  'school_management.school_name'), readonly=True)
    class_ids = fields.One2many(comodel_name="school.class", inverse_name="teacher_id",
                                string="Class ids")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee ID")
    user_id = fields.Many2one(comodel_name="res.users", string="User ID")

    def create_user(self):
        user = self.env["res.users"].create(
            {"login": self.email,
             "email": self.email,
             "name": self.name,
             "password": self.name}
        )
        print("user id : ", user)
        return user

    def create_employee(self):
        user = self.create_user()
        self.user_id = user.id
        employee = self.env["hr.employee"].create(
            {"work_email": self.email,
             "name": self.name,
             "user_id": user.id
             }
        )
        print("employee id : ", employee)
        return employee

    @api.model
    def create(self, vals):
        # create a new teacher
        teacher = super(SchoolTeacher, self).create(vals)
        # create new employee and affect it to teacher
        teacher.employee_id = teacher.create_employee()
        # add a group to this user
        group = self.env.ref('school_management.group_school_teacher')
        teacher.employee_id.user_id.groups_id += group

        return teacher

    _sql_constraints = [
        ('employee_uniq', 'unique (employee_id)',
         "An employee cannot be linked to multiple teachers in the same school.")
    ]

    def action_open_teacher_employee(self):
        # print("id : ", self.employee_id.id)
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Teachers',
        #     'res_model': 'hr.employee',
        #     'domain': [('id', '=', self.employee_id.id)],
        #     'view_mode': 'tree',
        #     'target': 'current'
        # }
        return self.employee_id
