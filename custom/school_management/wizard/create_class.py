from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime


class CreateClassWizard(models.TransientModel):
    _name = "school.class.wizard"
    _description = "Class Wizard"

    class_id = fields.Many2one(comodel_name="school.class", string="Class Id")

    def confirm_class(self):
        print('wizard..........................')
        active_id = self.env.context.get('active_id')
        student = self.env['school.student'].browse(active_id)
        print("active_id : ", active_id, "   student : ", student)
        if self.class_id.remaining_seats > 0:
            # write change
            student.class_id = self.class_id
            student.state = 'approved'
            student.admission_date = datetime.date.today()

            # create new user for the student
            student.user_id = student.create_user()
            print("student.user_id  : ", student.user_id, type(student.user_id))
            # add a group to this user
            group = self.env.ref('school_management.group_school_student')
            student.user_id.groups_id += group

        else:
            raise ValidationError("No more seats available in this class, choose another one")