# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models, _


class SchoolStudent(models.Model):
    _name = "school.student"
    # _inherits = {'res.partner': 'partner_id'}
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Student"

    school_name = fields.Char(string="School Name", default="West High School", readonly=True)
    academic_year = fields.Char(string="Academic Year")
    student_ref = fields.Char(string='Student ID', copy=False, readonly=True, required=True,
                              default=lambda self: _('New'))
    # Admission Request fields
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='full_name')
    picture = fields.Binary(string='Picture')
    code = fields.Char(string='Student Code')
    roll_number = fields.Char(string='Roll number')
    street1 = fields.Char(string='Street1')
    street2 = fields.Char(string='Street2')
    country = fields.Char(string='Country')
    city = fields.Char(string='City')
    state_adress = fields.Char(string='State')
    zip_code = fields.Char(string='Zip Code')
    phone_number = fields.Char(string='Phone Number')
    mobile_number = fields.Char(string='Mobile Number')
    email = fields.Char(string='Email', required=True)

    # Student Request fields
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], required=True, default='male')
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='get_age')
    admission_date = fields.Date(string='Admission Date')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('others', 'Others')
    ], required=True, default='single')
    remarks = fields.Char(string='Remarks')
    state = fields.Selection([('new', 'New'), ('approved', 'Approved'), ('alumni', 'Alumni'),
                              ('terminate', 'Terminate'), ('cancel', 'Cancelled')],
                             string='Status', default="new")

    class_id = fields.Many2one(comodel_name='school.class', string='Class')
    # student_id = fields.Many2one(comodel_name='school.student', string='Student')
    standard_id = fields.Many2one(comodel_name="school.standard", string='Standard')
    user_id = fields.Many2one(comodel_name='res.users', string='Student user')

    # related='res.users.id', related_sudo=True,
    # compute_sudo=True, store=True, readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('student_ref', _('New')) == _('New'):
            seq_date = str(datetime.date.today().year)+"/"+str(datetime.date.today().month)+"/"
            vals['student_ref'] = seq_date+self.env['ir.sequence'].next_by_code('school.student') or _('New')
        res = super(SchoolStudent, self).create(vals)
        print("vals ============> ", vals['student_ref'] )
        print("res =============> ", res)
        return res

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def create_user(self):
        vals = {
            "login": self.email,
            "name": self.name
        }
        user_id = self.env["res.users"].create(vals)
        return user_id

    def action_approved(self):
        for rec in self:
            # check age
            admission_age = self.env['ir.config_parameter'].sudo().get_param('school_management.student_admission_age')
            print("adm age ", admission_age, ' age : ', rec.age, " res : ", int(admission_age) == int(rec.age))
            if int(admission_age) == int(rec.age):
                rec.state = 'approved'
                rec.admission_date = datetime.date.today()
                # create new student user
                self.user_id = self.create_user()
                # add a group to this user
                group = self.env.ref('school_management.group_school_student')
                self.user_id.groups_id += group
            else:
                rec.state = 'cancel'

    def action_alumni(self):
        for rec in self:
            rec.state = 'alumni'

    def action_terminate(self):
        for rec in self:
            rec.state = 'terminate'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def full_name(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.name = rec.first_name + ' ' + rec.last_name
            else:
                rec.name = ''

    def get_age(self):
        for rec in self:
            today = datetime.date.today()
            if rec.birth_date:
                born = rec.birth_date
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                age = 0
            rec.age = age
            # print("birth date : ", born, " today : ", today, " age : ", rec.age)

    @api.onchange('birth_date')
    def on_change_birth_date(self):
        for rec in self:
            rec.get_age()

