# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime
import dateutil.relativedelta
from odoo.exceptions import ValidationError

class hr_expense(models.Model):
    _inherit = 'hr.expense'
#     _name = 'odoo_travel_epenses.odoo_travel_epenses'


    is_travel = fields.Boolean()
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    free_food_num = fields.Integer()
    total_travel = fields.Float(digits=(18, 6))
    first_day_hours = fields.Float(digits=(18, 6))
    last_day_hours = fields.Float(digits=(18, 6))
    full_day_num = fields.Integer()
    first_day_allowance = fields.Float(digits=(18, 6))
    last_day_allowance = fields.Float(digits=(18, 6))
    full_day_allowance = fields.Float(digits=(18, 6))

    @api.onchange('date_to','date_from','free_food_num')
    def _onchange_date_to_date_from_free_food_num(self):
        exp_min=self.env.user.company_id.exp_min
        exp_mid=self.env.user.company_id.exp_mid
        exp_max=self.env.user.company_id.exp_max
        if self.date_from and self.date_to:
            nahrada_dny=0
            nahrada_hodiny=0
            nahrada_hodiny_last=0
            nahrada_dny=0
            nahrada_hodiny_first=0
            first_day_hours=0
            duration_remain=0
            last_day_hours=0
            duration_days=0
            celkem=0
            duration = self.date_to-self.date_from
            duration_days = duration.days-1
            #print("duration days %s" % duration_days)
            date_to_mid = self.date_to + dateutil.relativedelta.relativedelta(hour=0, minute=0, second=0)
            # výpočet začátku služební cesty, days=-3 znamená že odečte od teď tři dny, hour=11 znamená, že nastaví hodiny na 11:00 Tzn služební cesta začne před tremi dny v jedenác dopoledne.
            date_from_mid = self.date_from + dateutil.relativedelta.relativedelta(days=1, hour=0, minute=0, second=0)
            # maximální počet jídel pro all day je 4 když vyjdou na den 4 a víc jídel je srážka rovná příplatku (259-259)
            if self.free_food_num > 0:
                if duration_days > 0 and self.free_food_num > 0:
                    all_days_free_day = int(self.free_food_num/duration_days)
                    if all_days_free_day > 4:
                        free_food_to_first_or_last_day = (all_days_free_day-4)*duration_days
                        all_days_free_day = 4
                    else:
                        free_food_to_first_or_last_day = False
                    if free_food_to_first_or_last_day:
                        all_days_free_addday = (self.free_food_num % duration_days)+free_food_to_first_or_last_day
                    else:
                        all_days_free_addday = (self.free_food_num % duration_days)
                    all_days_free_food = all_days_free_day*duration_days
                    free_food_price = all_days_free_food*0.25*exp_max
                    #print("num food per day %s" % all_days_free_day)
                    #print("modulo food per day %s" % all_days_free_addday)
                    #print("all days num days free food %s" % all_days_free_food)
                else:
                    all_days_free_day = 0
                    all_days_free_food = 0
                    free_food_price = 0
                    all_days_free_addday = 0
                #print("food price %s" % free_food_price)
            else:
                all_days_free_food = 0
                all_days_free_day = 0
                free_food_price = 0
                all_days_free_addday = 0

            if duration_days >= 0:
                first_day_free_food = int((all_days_free_addday)/2)
                #print("first day %s" % first_day_free_food)
                last_day_free_food = int(self.free_food_num-first_day_free_food-all_days_free_food)
                #print("last day %s" % last_day_free_food)
                nahrada_dny = duration_days*exp_max
                if free_food_price:
                    nahrada_dny = nahrada_dny-free_food_price
                first_day_duration = date_from_mid - self.date_from
                first_day_hours = float(first_day_duration.total_seconds()/3600)
                if first_day_hours:
                    nahrada_hodiny_first=0
                    if first_day_hours > 5.0:
                        nahrada_hodiny_first = exp_min
                        if first_day_free_food > 1:
                            nahrada_hodiny_first = 0.0
                        else:
                            if first_day_free_food > 0:
                                nahrada_hodiny_first = nahrada_hodiny_first - \
                                    (first_day_free_food*0.7*nahrada_hodiny_first)
                        if first_day_hours > 12.0:
                            if first_day_hours > 18.0:
                                nahrada_hodiny_first = exp_max
                                if first_day_free_food > 0:
                                    nahrada_hodiny_first = nahrada_hodiny_first - \
                                        (first_day_free_food*0.25*nahrada_hodiny_first)
                            else:
                                nahrada_hodiny_first = exp_mid
                                if first_day_free_food > 2:
                                    nahrada_hodiny_first = 0.0
                                else:
                                    if first_day_free_food > 0:
                                        nahrada_hodiny_first = nahrada_hodiny_first - \
                                            (first_day_free_food*0.35*nahrada_hodiny_first)
                    # print(self.nahrada_hodiny_first)
                last_day_duration = self.date_to - date_to_mid
                last_day_hours = float(last_day_duration.total_seconds()/3600)
                if last_day_hours:
                    nahrada_hodiny_last=0
                    if last_day_hours > 5.0:
                        if last_day_free_food > 1:
                            nahrada_hodiny_last = 0.0
                        if last_day_hours > 12.0:
                            if last_day_hours > 18.0:
                                if nahrada_hodiny_last:
                                    nahrada_hodiny_last = nahrada_hodiny_last+exp_max
                                else:
                                    nahrada_hodiny_last = exp_max
                                if last_day_free_food > 0:
                                    nahrada_hodiny_last = nahrada_hodiny_last - \
                                        (last_day_free_food*0.25*nahrada_hodiny_last)
                            else:
                                nahrada_hodiny_last = nahrada_hodiny_last+exp_mid
                                if last_day_free_food > 2:
                                    nahrada_hodiny_last = 0.0
                                else:
                                    if last_day_free_food > 0:
                                        nahrada_hodiny_last = nahrada_hodiny_last - \
                                            (last_day_free_food*0.35*nahrada_hodiny_last)
                        if last_day_hours <= 12.0:
                            nahrada_hodiny_last = nahrada_hodiny_last+exp_min
                            if last_day_free_food > 0:
                                nahrada_hodiny_last = nahrada_hodiny_last - \
                                    (last_day_free_food*0.7*nahrada_hodiny_last)

                    # print(self.nahrada_hodiny_last)
                    nahrada_hodiny =nahrada_hodiny_first+nahrada_hodiny_last
                    # print(self.nahrada_hodiny)

            else:
                nahrada_dny=0
                duration_remain = float(duration.total_seconds()/3600)
                if duration_remain:
                    if duration_remain > 5.0:
                        if duration_remain > 12.0:
                            if duration_remain > 18.0:
                                nahrada_hodiny = nahrada_hodiny+exp_max-free_food_price
                                if self.free_food_num >= 4:
                                    nahrada_hodiny = 0.0
                            else:
                                nahrada_hodiny = nahrada_hodiny+exp_mid-free_food_price
                                if self.free_food_num > 2:
                                    nahrada_hodiny = 0.0
                        else:
                            nahrada_hodiny = nahrada_hodiny+exp_min-free_food_price
                            if self.free_food_num > 1:
                                nahrada_hodiny = 0.0

            celkem = nahrada_dny+nahrada_hodiny
            if nahrada_hodiny_first:
                self.first_day_allowance=nahrada_hodiny_first
            else:
                self.first_day_allowance=nahrada_hodiny
            self.last_day_allowance=nahrada_hodiny_last
            self.full_day_allowance=nahrada_dny

            if first_day_hours:
                self.first_day_hours=first_day_hours
            else:
                self.first_day_hours=duration_remain

            self.last_day_hours=last_day_hours
            self.full_day_num=duration_days

            self.total_travel=celkem
            self.unit_amount=celkem


    def is_free_day(self):
        if self.date_to and self.date_from:
            empl_id=self.employee_id.id

            date_to=self.date_to.date()
            date_from=self.date_from.date()
            leave=self.env['account.analytic.line'].search([('employee_id', '=', empl_id), ('holiday_id', '!=', None), ('date', '<', date_to),('date', '>', date_from) ])

            if int(len(leave))>0:
                return True
            else:
                return False

    @api.constrains('date_from', 'date_to')
    def _validate_date(self):
        for record in self:
           if record.is_free_day()==True:
                raise ValidationError(_("There are some leaves in selected date range. Please change date range."))
