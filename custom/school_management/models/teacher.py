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
    user_id = fields.Many2one(comodel_name='res.users', string='Teacher user')

    def create_user(self):
        user_id = self.env["res.users"].create(
            {"login": self.email, "name": self.name}
        )
        return user_id

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
