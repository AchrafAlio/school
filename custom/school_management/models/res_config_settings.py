# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    student_admission_age = fields.Integer(string='Student Admission Age',
                                           config_parameter="school_management.student_admission_age")
