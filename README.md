# odoo_timesheets_to_attendance
docházka generovaná na základě vykázaných timesheetů


připojení do stroje:

docker exec -u 0 -it 6fbf31dba1f2  /bin/bash

připojení do běžící odoo databáze:

odoo shell -d "UGexpHR"



pokud zapisuju data musím na konci použít

self.env.cr.commit()

aby se to zapsalo do databáze


projekt generování docházky
nastavení: Vybrat který typy práce se mají zahrnout do časového rámce pro výpočet docházky.

import operator
from datetime import datetime

self.env["hr.attendance"].search_read()


Attendance=self.env['hr.attendance']

check_in_str='18/08/2022 08:00:00'

check_out_str='18/08/2022 12:00:00'


check_in_date=datetime.strptime(check_in_str, '%d/%m/%Y %H:%M:%S')
check_out_date=datetime.strptime(check_out_str, '%d/%m/%Y %H:%M:%S')

new=Attendance.create({'employee_id':'1' , 'check_in': check_in_date, 'check_out': check_out_date})



příkaz pro vyhledávání: - tady bude muset přibýt sčítač hodin práce a práce přesčas po dnech a zaměstnancích

práce na projektu id=6

ts=self.env["account.analytic.line"].search_read([('heo_id','>','0'),('odoo_sync_date','>','2022-05-01'),"&",('odoo_sync_date','<','2022-06-01'), ('work_type_id','in',(6,8))])

práce přesčas id=8

přičíst přesčasy k základnímu času timesheetů

ts.sort(key=operator.intemgetter('employee_id','date'))



import pandas

table=pandas.DataFrame.from_dict(ts)

table.groupby(['employee_id','date'], as_index=False)["unit_amount"].sum()

dict=table.to_dict('records')



načtení pracovního kalendáře pro zaměstnance: tady musím počítat s podmínkou, že když jeden den přesáhnu určitý počet hodin to co zbyde musím přidat k počáteční hodině. Musí mít čas na spánek.

administrator_id=1
empl=self.env['hr.employee'].search_read([('id','=','1')])
calendar_id=empl[0].get('resource_calendar_id')

resource_cal=self.env['resource.calendar'].search_read([('id','=','1')])




vytvoření pracovních hodin od do:
resource_cal_attendance=self.env['resource.calendar.attendance'].search_read([('calendar_id','=', '1')])
for rec in resource_cal_attendance:
...     rec.sort(key=lambda x: x.get('dayofweek'))
...     print(rec)

výpis přímo z calendar.attendance
resource_cal_attendance=self.env['resource.calendar.attendance'].search_read([('calendar_id','=', 'Výchozí')])

řazení kalendáře podle dní v týdnu a hodin od

s=sorted(resource_cal_attendance, key=operator.itemgetter('dayofweek', 'hour_from'))