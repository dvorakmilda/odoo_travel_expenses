# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
import operator
import pandas
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


#self.env["account.analytic.line"].search_read([('heo_id','>','0'),('odoo_sync_date','>','2022-05-01'),"&",('odoo_sync_date','<','2022-06-01'), ('work_type_id','=',6)])


class hr_attendance(models.Model):
    _inherit = 'hr.attendance'

    @api.multi
    def create_lastmonth_attendance(self):

        now=datetime.today()
        date_from = datetime(now.year, now.month, 1) + relativedelta(months=-1)
        date_to = datetime(now.year, now.month, 1) + relativedelta(minutes=-1)

        ts=self.env["account.analytic.line"].search_read([('heo_id','>','0'),('odoo_sync_date','>=',date_from),"&",('odoo_sync_date','<=',date_to), ('work_type_id','in',(6,8))])

        return ts

