# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
import operator
import pandas
import random
from pytz import timezone
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


                    #!!!! přidat taky rozlišování na minuty zatím je to jenom na hodiny
                    #!!!! upravit načítání timezone podle uživatele vazba přes employee_id


class hr_attendance(models.Model):
    _inherit = 'hr.attendance'

    def create_lastmonth_attendance(self):

        now=datetime.today()
        date_from = datetime(now.year, now.month, 1) + relativedelta(months=-1)
        date_to = datetime(now.year, now.month, 1) + relativedelta(minutes=-1)

        ts=self.env["account.analytic.line"].search_read([('heo_id','>','0'),('date','>=',date_from),"&",('date','<=',date_to), ('work_type_id','in',(6,8))])

        ts.sort(key=operator.itemgetter('employee_id','date'))

        self.table=pandas.DataFrame.from_dict(ts)

        self.table.groupby(['employee_id','date'], as_index=False)["unit_amount"].sum()
        group_by=(self.table.groupby(['employee_id','date'], as_index=False)["unit_amount"].sum())
        self.dictionary=group_by.to_dict('records')

        for rec in self.dictionary:

            #print('Zacatek smyčky',rec['employee_id'], rec['date'], rec['date'].strftime('%w'), rec['unit_amount'])
            empl=self.env['hr.employee'].search_read([('id','=',rec['employee_id'][0])])

            calendar_id=empl[0].get('resource_calendar_id')[1]
            resource_cal_attendance=self.env['resource.calendar.attendance'].search_read([('calendar_id','=', calendar_id)])
            res_calendar_att_sorted=sorted(resource_cal_attendance, key=operator.itemgetter('dayofweek', 'hour_from'))
            total_time=rec['unit_amount']
            day_parts=[]
            for day_part in res_calendar_att_sorted:
                if rec['date'].strftime('%w')==day_part['dayofweek']:
                    if day_part not in day_parts:
                        day_parts.append(day_part)
                        #print('Day of week',day_part['dayofweek'], day_part['day_period'] )

#            print(day_parts)
            for part in day_parts:
                if total_time>0 :
                    #!!!! přidat taky rozlišování na minuty zatím je to jenom na hodiny
                    h_in=int(part['hour_from'])
                    h_out=int(part['hour_to'])
                    work_hours=int(part['hour_to'])- int(part['hour_from'])
                    utc_check_in_date=rec['date']+relativedelta(hours=h_in)
                    utc_check_out_date=rec['date']+relativedelta(hours=h_out)
                    tz_local=timezone('Europe/Prague')
                    self.check_in_date=tz_local.localize(utc_check_in_date)
                    self.check_out_date=tz_local.localize(utc_check_out_date)
             #       print('Zápis attendance', rec['date'],'total_time', total_time, h_in,h_out, self.check_in_date, self.check_out_date )
                    self._cr.execute('INSERT INTO hr_attendance (employee_id, check_in,check_out, worked_hours, create_date, create_uid) VALUES (%s, %s, %s, %s, %s,%s)', (rec['employee_id'][0],self.check_in_date,self.check_out_date, work_hours, datetime.now(),'1'))


#                    attendance_id=self.env['hr.attendance'].create({
#                        'employee_id':rec['employee_id'][0] ,
#                        'check_in': self.check_in_date,
#                        'check_out': self.check_out_date
#                        } )
#                    print(attendance_id)

                    total_time=total_time-( int(part['hour_to'])- int(part['hour_from'] ) )

            if total_time > 0:
                new_check_out_date=self.check_out_date + relativedelta(hours=int(total_time))
                self.check_in_date=self.check_out_date
              #  print('Dodatečný zápis attendance', rec['date'],total_time, part['dayofweek'],h_in,h_out, self.check_in_date, new_check_out_date )
                self._cr.execute('INSERT INTO hr_attendance (employee_id, check_in,check_out,worked_hours,create_date,create_uid) VALUES (%s, %s, %s,%s,%s,%s)', (rec['employee_id'][0],self.check_in_date,new_check_out_date , total_time, datetime.now(),'1'))

#                attendance_id=self.env['hr.attendance'].create({
#                    'employee_id':rec['employee_id'][0] ,
#                    'check_in': self.check_in_date,
#                    'check_out': new_check_out_date} )
                total_time=0
