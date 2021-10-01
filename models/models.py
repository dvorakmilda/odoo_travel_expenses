# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
import dateutil.relativedelta

class hr_expense(models.Model):
    _inherit = 'hr.expense'
#     _name = 'odoo_travel_epenses.odoo_travel_epenses'


    is_travel = fields.Boolean()
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    free_food_num = fields.Integer(default=0)
    total_travel = fields.Float(digits=(18, 6), readonly=True)
    first_day_hours = fields.Float(digits=(18, 6), readonly=True)
    last_day_hours = fields.Float(digits=(18, 6), readonly=True)
    full_day_num = fields.Integer( readonly=True)
    first_day_allowance = fields.Float(digits=(18, 6), readonly=True)
    last_day_allowance = fields.Float(digits=(18, 6), readonly=True)
    full_day_allowance = fields.Float(digits=(18, 6), readonly=True)

    @api.onchange('date_to','date_from','free_food_num')
    def _onchange_date_to_date_from_free_food_num(self):
        nahrada_dny = 0.0
        nahrada_hodiny = 0.0
        nahrada_hodiny_first = 0.0
        nahrada_hodiny_last = 0.0
        free_food_price = False
        if self.date_from and self.date_to:
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
                    free_food_price = all_days_free_food*0.25*259
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
                nahrada_dny = duration_days*259
                if free_food_price:
                    nahrada_dny = nahrada_dny-free_food_price
                first_day_duration = date_from_mid - self.date_from
                first_day_hours = float(first_day_duration.total_seconds()/3600)
                if first_day_hours:
                    if first_day_hours > 5.0:
                        nahrada_hodiny_first = 108
                        if first_day_free_food > 1:
                            nahrada_hodiny_first = 0.0
                        else:
                            if first_day_free_food > 0:
                                nahrada_hodiny_first = nahrada_hodiny_first - \
                                    (first_day_free_food*0.7*nahrada_hodiny_first)
                        if first_day_hours > 12.0:
                            if first_day_hours > 18.0:
                                nahrada_hodiny_first = 259
                                if first_day_free_food > 0:
                                    nahrada_hodiny_first = nahrada_hodiny_first - \
                                        (first_day_free_food*0.25*nahrada_hodiny_first)
                            else:
                                nahrada_hodiny_first = 167
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
                    if last_day_hours > 5.0:
                        if last_day_free_food > 1:
                            nahrada_hodiny_last = 0.0
                        if last_day_hours > 12.0:
                            if last_day_hours > 18.0:
                                nahrada_hodiny_last = nahrada_hodiny_last+259
                                if last_day_free_food > 0:
                                    nahrada_hodiny_last = nahrada_hodiny_last - \
                                        (last_day_free_food*0.25*nahrada_hodiny_last)
                            else:
                                nahrada_hodiny_last = nahrada_hodiny_last+167
                                if last_day_free_food > 2:
                                    nahrada_hodiny_last = 0.0
                                else:
                                    if last_day_free_food > 0:
                                        nahrada_hodiny_last = nahrada_hodiny_last - \
                                            (last_day_free_food*0.35*nahrada_hodiny_last)
                        if last_day_hours <= 12.0:
                            nahrada_hodiny_last = nahrada_hodiny_last+108
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
                                nahrada_hodiny = nahrada_hodiny+259-free_food_price
                                if self.free_food_num >= 4:
                                    nahrada_hodiny = 0.0
                            else:
                                nahrada_hodiny = nahrada_hodiny+167-free_food_price
                                if self.free_food_num > 2:
                                    nahrada_hodiny = 0.0
                        else:
                            nahrada_hodiny = nahrada_hodiny+108-free_food_price
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

             #duration_days
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


#     _inherit = ''