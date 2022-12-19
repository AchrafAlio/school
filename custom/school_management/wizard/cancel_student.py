from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CreateClassWizard(models.TransientModel):
    _name = "school.cancel.student.wizard"
    _description = "Cancel Student Wizard"

    remarks = fields.Char(string="Remarks")

    def confirm_class(self):
        print('wizard')
        active_id = self.env.context.get('active_id')
        rec = self.env['school.student'].browse(active_id)
        if rec.remarks:
            rec.remarks = str(rec.remarks) + '\n' + str(self.remarks)
        else:
            rec.remarks = str(self.remarks)
        rec.state = 'cancel';
