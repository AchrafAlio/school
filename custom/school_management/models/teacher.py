# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = 'hr.employee'
    _description = "School Teacher"

    name = fields.Char(string='Teacher Name', required=True)
    email = fields.Char(string='Teacher email', required=True)
    picture = fields.Binary(string='Picture')
    subject_id = fields.Many2one(comodel_name='school.subject', string='Subject')
    school_name = fields.Char(string="School Name", store=False,
                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                  'school_management.school_name'))
    class_ids = fields.One2many(comodel_name="school.class", inverse_name="teacher_id",
                                string="Class ids")
    # employee_id = fields.Many2one(comodel_name="hr.empoyee", string="Employee ID")
    # user_id = fields.Many2one(comodel_name='hr.employee', string='Teacher user')
    # hr_id = fields.Many2one(comodel_name='hr.employee', string='Teacher hr')
    category_ids = fields.Char("Category ids")

    def create_user(self):
        user_id = self.env["res.users"].create(
            {"login": self.email, "name": self.name, "password": self.name}
        )
        return user_id

    #
    # def create_hr(self):
    #     hr_id = self.env["hr.employee"].create(
    #         {"work_email": self.email,
    #          "name": self.name,
    #          "user_id": self.user_id.id,
    #          }
    #     )
    #     return hr_id
    #   -
    @api.model
    def create(self, vals):
        # create a new teacher
        res = super(SchoolTeacher, self).create(vals)
        # create new Teacher user
        res.user_id = res.create_user()
        # add a group to this user
        group = self.env.ref('school_management.group_school_teacher')
        res.user_id.groups_id += group
        return res
