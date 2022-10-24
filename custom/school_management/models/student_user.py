from odoo import api, fields, models


class SchoolStudentUser(models.Model):
    # _name = "school.student"
    _inherit = 'school.student'
    _description = "School Student User"

    user_id = fields.Many2one(comodel_name='res.users', string='Student user')
                              # related='res.users.id', related_sudo=True,
                              # compute_sudo=True, store=True, readonly=True)
    # @api.model
    # def create(self, vals):
    #     return super('school.student', self).create(vals)