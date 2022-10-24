from odoo import api, fields, models


class SchoolStudentUser(models.Model):
    # _name = "school.student"
    _inherit = 'school.student'
    _description = "School Student User"

    # @api.model
    # def create(self, vals):
    #     return super('school.student', self).create(vals)