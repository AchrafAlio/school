from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = ['hr.employee']

    teacher_id = fields.One2many(comodel_name="school.teacher", inverse_name="employee_id", string="Related Teacher")
    name = fields.Char(related='teacher_id.name', readonly=False)
    email = fields.Char(related='teacher_id.email', readonly=False)
    subject_id = fields.Many2one(comodel_name='school.subject', string='Subject', related='teacher_id.subject_id')
    school_name = fields.Char(string="School Name", related='teacher_id.school_name')

    def get_teacher_employee(self):
        print("click smart button")
