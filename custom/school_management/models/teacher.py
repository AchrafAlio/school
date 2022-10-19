# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Teacher"

    name = fields.Char(string='Teacher Name', required=True, tracking=True)
    picture = fields.Binary(string='Picture')
    subject_id = fields.Many2one(comodel_name='school.subject', string='Subject')
