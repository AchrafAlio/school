# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Teacher"

    name = fields.Char(string='Teacher Name', required=True)
    email = fields.Char(string='Teacher email', required=True)
    picture = fields.Binary(string='Picture')
    school_name = fields.Char(string="School Name",
                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                  'school_management.school_name'), readonly=True)
    subject_id = fields.Many2one(comodel_name='school.subject', string='Subject')
    class_ids = fields.Many2many(comodel_name="school.class", string="Class ids")
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

        # check constraint : the subject must be not redundant in the same class
        print("subject_id : ", teacher.subject_id, "class_ids", teacher.class_ids)
        for cl in teacher.class_ids:
            # clas = self.env['school.class'].sudo().browse(cl)
            # print("class--------------> ", clas)
            print(cl, cl.sequence, cl.subject_ids)
            if teacher.subject_id in cl.subject_ids:
                print(">>>>>>>>>>>>>>>>>>>>>>>>Redundance")
                print(teacher.subject_id, " is affected to another teacher ")
                raise ValidationError("Subject ( "+str(teacher.subject_id.name)+
                                      " ) is affected to another teacher in Class ( "+str(cl.sequence)+" )")
            else:
                cl.subject_ids += teacher.subject_id

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
