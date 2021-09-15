# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_expense(models.Model):
    _inherit = 'hr_expense'
#     _name = 'odoo_travel_epenses.odoo_travel_epenses'


    is_travel = fields.Boolean()
    date_from = fields.Datetime()
    date_from = fields.Datetime()
    free_food_num = fields.Integer()
    total_travel = fields.Float( digits=(18, 6))
    first_day_hours = fields.Float( digits=(18, 6))
    last_day_hours = fields.Float( digits=(18, 6))
    full_day_num = fields.Integer()         #duration_days
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


#     _inherit = ''