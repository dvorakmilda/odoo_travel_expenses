# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
import operator
import pandas
import dateutil.relativedelta
from odoo.exceptions import ValidationError

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    attendance_calendar_id = fields.Many2one(
        'resource.calendar', string='Attendance calendar',
        default=lambda self: self.env['res.company']._company_default_get().resource_calendar_id.id)

