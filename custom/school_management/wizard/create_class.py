from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CreateClassWizard(models.TransientModel):
    _name = "school.class.wizard"
    _description = "Class Wizard"

    class_id = fields.Many2one(comodel_name="school.class", string="Class Id")

    def confirm_class(self):
        print('wizard')
        active_id = self.env.context.get('active_id')
        student_id = self.env['school.student'].browse(active_id)
        if self.class_id.remaining_seats > 0:
            # write change
            student_id.class_id = self.class_id
            student_id.state = 'approved'
        else:
            raise ValidationError("No more seats available in this class, choose another one")

        # record.state = 'approved'
