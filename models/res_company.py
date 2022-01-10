# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'

    exp_min = fields.Float(string='', digits=(18, 6), default=108)
    exp_mid = fields.Float(string='', digits=(18, 6), default=167)
    exp_max = fields.Float(string='', digits=(18, 6), default=259)


