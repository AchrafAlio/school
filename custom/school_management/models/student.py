# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = "school.student"
    # _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Student"

    # Admission Request fields
    first_name = fields.Char(string='First Name', required=True, tracking=True)
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
    email = fields.Char(string='Email')

    # Student Request fields
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], required=True, default='male', tracking=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age')
    admission_date = fields.Date(string='Admission Date')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('others', 'Others')
    ], required=True, default='single', tracking=True)
    remarks = fields.Char(string='Remarks')

    class_id = fields.Many2one(comodel_name='school.class', string='Class')
    student_id = fields.Many2one(comodel_name='school.student', string='Student')

    state = fields.Selection([('new', 'New'), ('approved', 'Approved'), ('alumni', 'Alumni'),
                              ('terminate', 'Terminate'), ('cancel', 'Cancelled')],
                             string='Status', tracking=True, default="new")

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_approved(self):
        for rec in self:
            rec.state = 'approved'

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
            rec.name = rec.first_name + ' ' + rec.last_name
