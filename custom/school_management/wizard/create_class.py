from odoo import api, fields, models, _


class CreateClassWizard(models.TransientModel):
    _name = "school.class.wizard"
    _description = "Class Wizard"

    class_id = fields.Many2one(comodel_name="school.class", string="Class Id")

    def confirm_student(self):
        print('wizard')
        active_id = self.env.context.get('active_id')
        record = self.env['school.student'].browse(active_id)
        record.class_id = self.class_id
        record.state = 'approved'
