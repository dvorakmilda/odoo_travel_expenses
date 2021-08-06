import datetime
import dateutil.relativedelta


class Calculate():
    def __init__(self):
        #todo - místo konstanty částky pro daná časová období udělat načítání z pole z databáze
        #data datumy pro potřeby testu
        self.x_date_to = datetime.datetime.now() 
        self.x_date_to_mid = self.x_date_to + dateutil.relativedelta.relativedelta(hour=0, minute=0, second=0)
        self.x_date_from = self.x_date_to + dateutil.relativedelta.relativedelta(days=-3, hour=11, minute=0, second=0) #výpočet začátku služební cesty, days=-3 znamená že odečte od teď tři dny, hour=11 znamená, že nastaví hodiny na 11:00 Tzn služební cesta začne před tremi dny v jedenác dopoledne. 
        self.x_date_from_mid = self.x_date_from + \
            dateutil.relativedelta.relativedelta(days=1, hour=0, minute=0, second=0)
        self.x_total_free_food = 0 #konstanta bude známá z formuláře

    def calculate(self):
        free_food_price = False
        if self.x_date_from and self.x_date_to:
            duration = self.x_date_to-self.x_date_from
            duration_days = duration.days-1
            #print("duration days %s" % duration_days)
            self.nahrada_hodiny = 0.0
            self.nahrada_hodiny_first = 0.0
            self.nahrada_hodiny_last = 0.0
            # maximální počet jídel pro all day je 4 když vyjdou na den 4 a víc jídel je srážka rovná příplatku (259-259)
            if self.x_total_free_food > 0:
                if duration_days > 0 and x_total_free_food >0:
                    all_days_free_day = int(self.x_total_free_food/duration_days)
                    if all_days_free_day > 4:
                        free_food_to_first_or_last_day = (all_days_free_day-4)*duration_days
                        all_days_free_day = 4
                    else:
                        free_food_to_first_or_last_day = False
                    if free_food_to_first_or_last_day:
                        all_days_free_addday = (self.x_total_free_food % duration_days)+free_food_to_first_or_last_day
                    else:
                        all_days_free_addday = (self.x_total_free_food % duration_days)
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
                last_day_free_food = int(self.x_total_free_food-first_day_free_food-all_days_free_food)
                #print("last day %s" % last_day_free_food)
                self.nahrada_dny = duration_days*259
                if free_food_price:
                    self.nahrada_dny = self.nahrada_dny-free_food_price
                first_day_duration = self.x_date_from_mid - self.x_date_from
                first_day_hours = first_day_duration.total_seconds()/3600
                if first_day_hours:
                    if first_day_hours > 5:
                        self.nahrada_hodiny_first = 108
                        if first_day_free_food > 1:
                            self.nahrada_hodiny_first = 0.0
                        else:
                            if first_day_free_food > 0:
                                self.nahrada_hodiny_first = self.nahrada_hodiny_first - \
                                    (first_day_free_food*0.7*self.nahrada_hodiny_first)
                        if first_day_hours > 12:
                            if first_day_hours > 18:
                                self.nahrada_hodiny_first = 259
                                if first_day_free_food > 0:
                                    self.nahrada_hodiny_first = self.nahrada_hodiny_first - \
                                        (first_day_free_food*0.25*self.nahrada_hodiny_first)
                            else:
                                self.nahrada_hodiny_first = 167
                                if first_day_free_food > 2:
                                    self.nahrada_hodiny_first = 0.0
                                else:
                                    if first_day_free_food > 0:
                                        self.nahrada_hodiny_first = self.nahrada_hodiny_first - \
                                            (first_day_free_food*0.35*self.nahrada_hodiny_first)
                    #print(self.nahrada_hodiny_first)
                last_day_duration = self.x_date_to - self.x_date_to_mid
                last_day_hours = last_day_duration.total_seconds()/3600
                if last_day_hours:
                    if last_day_hours > 5:
                        if last_day_free_food > 1:
                            self.nahrada_hodiny_last = 0.0
                        if last_day_hours > 12:
                            if last_day_hours > 18:
                                self.nahrada_hodiny_last = self.nahrada_hodiny_last+259
                                if last_day_free_food > 0:
                                    self.nahrada_hodiny_last = self.nahrada_hodiny_last - \
                                        (last_day_free_food*0.25*self.nahrada_hodiny_last)
                            else:
                                self.nahrada_hodiny_last = self.nahrada_hodiny_last+167
                                if last_day_free_food > 2:
                                    self.nahrada_hodiny_last = 0.0
                                else:
                                    if last_day_free_food > 0:
                                        self.nahrada_hodiny_last = self.nahrada_hodiny_last - \
                                            (last_day_free_food*0.35*self.nahrada_hodiny_last)
                        if last_day_hours < 12:
                            self.nahrada_hodiny_last = self.nahrada_hodiny_last+108
                            if last_day_free_food > 0:
                                self.nahrada_hodiny_last = self.nahrada_hodiny_last - \
                                    (last_day_free_food*0.7*self.nahrada_hodiny_last)

                    #print(self.nahrada_hodiny_last)
                    self.nahrada_hodiny = self.nahrada_hodiny_first+self.nahrada_hodiny_last
                    #print(self.nahrada_hodiny)
            else:
                duration_days_in_hours = duration.days*24
                duration_hours = duration.total_seconds()/3600
                duration_remain = duration_hours-duration_days_in_hours
                self.nahrada_dny = 0
                if duration_remain:
                    if duration_remain > 5:
                        if duration_remain > 12:
                            if duration_remain > 18:
                                self.nahrada_hodiny = self.nahrada_hodiny+259-free_food_price
                                if self.x_total_free_food >= 4:
                                    self.nahrada_hodiny = 0.0
                            else:
                                self.nahrada_hodiny = self.nahrada_hodiny+167-free_food_price
                                if self.x_total_free_food > 2:
                                    self.nahrada_hodiny = 0.0
                        else:
                            self.nahrada_hodiny = self.nahrada_hodiny+108-free_food_price
                            if self.x_total_free_food > 1:
                                self.nahrada_hodiny = 0.0

        celkem = self.nahrada_dny+self.nahrada_hodiny

        print("Datum od %s" %self.x_date_from, "Datum do %s" %self.x_date_to)
        print("Náhrada hodiny %s" %self.nahrada_hodiny)
        print("Náhrada celé dny dny %s" %self.nahrada_dny)
        print("Náhrada celkem %s" %round(celkem, 0))


def main():
    calc = Calculate()
    calcul = calc.calculate()


if __name__ == '__main__':
    main()
