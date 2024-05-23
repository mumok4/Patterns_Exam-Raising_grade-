import time
import holidays
import math
import  datetime


class MonthlyCalendar:
    cal_ID = 0  # Define cal_ID as a class-level attribute

    def __init__(self, year=None, month=None):
        self.tFontFace = 'Arial, Helvetica'
        self.tFontSize = 12
        self.tFontColor = '#FFFFFF'
        self.tBGColor = '#304B90'

        self.hFontFace = 'Arial, Helvetica'
        self.hFontSize = 10
        self.hFontColor = '#FFFFFF'
        self.hBGColor = '#304B90'

        self.dFontFace = 'Arial, Helvetica'
        self.dFontSize = 12
        self.dFontColor = '#000000'
        self.dBGColor = '#FFFFFF'

        self.wFontFace = 'Arial, Helvetica'
        self.wFontSize = 10
        self.wFontColor = '#FFFFFF'
        self.wBGColor = '#304B90'

        self.saFontColor = '#0000D0'
        self.saBGColor = '#F6F6FF'

        self.suFontColor = '#D00000'
        self.suBGColor = '#FFF0F0'

        self.tdBorderColor = 'red'

        self.borderColor = '#304B90'
        self.hilightColor = '#FFFF00'

        self.link = ''
        self.offset = 2  # Start the week from Monday
        self.weekNumbers = 0

        self.weekdays = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')
        self.months = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                       'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

        self.error = ('Год должен быть в диапазоне 1 - 3999!', 'Месяц должен быть в диапазоне 1 - 12!')

        if year is None and month is None:
            year = time.localtime().tm_year
            month = time.localtime().tm_mon
        elif year is None and month is not None:
            year = time.localtime().tm_year
        elif month is None:
            month = 1

        self.year = int(year)
        self.month = int(month)
        self.specDays = {}
        self.holidays = []

        self.fetch_holidays()  # Fetch holidays for the given year and month

    __size = 0
    __mDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def set_styles(self):
        self.cal_ID += 1  # Increment the cal_ID for each instance
        html = f'<style> .cssTitle{self.cal_ID} {{ '
        if self.tFontFace: html += f'font-family: {self.tFontFace}; '
        if self.tFontSize: html += f'font-size: {self.tFontSize}px; '
        if self.tFontColor: html += f'color: {self.tFontColor}; '
        if self.tBGColor: html += f'background-color: {self.tBGColor}; '
        html += f'}} .cssHeading{self.cal_ID} {{ '
        if self.hFontFace: html += f'font-family: {self.hFontFace}; '
        if self.hFontSize: html += f'font-size: {self.hFontSize}px; '
        if self.hFontColor: html += f'color: {self.hFontColor}; '
        if self.hBGColor: html += f'background-color: {self.hBGColor}; '
        html += f'}} .cssDays{self.cal_ID} {{ '
        if self.dFontFace: html += f'font-family: {self.dFontFace}; '
        if self.dFontSize: html += f'font-size: {self.dFontSize}px; '
        if self.dFontColor: html += f'color: {self.dFontColor}; '
        if self.dBGColor: html += f'background-color: {self.dBGColor}; '
        html += f'}} .cssWeeks{self.cal_ID} {{ '
        if self.wFontFace: html += f'font-family: {self.wFontFace}; '
        if self.wFontSize: html += f'font-size: {self.wFontSize}px; '
        if self.wFontColor: html += f'color: {self.wFontColor}; '
        if self.wBGColor: html += f'background-color: {self.wBGColor}; '
        html += f'}} .cssSaturdays{self.cal_ID} {{ '
        if self.dFontFace: html += f'font-family: {self.dFontFace}; '
        if self.dFontSize: html += f'font-size: {self.dFontSize}px; '
        if self.saFontColor: html += f'color: {self.saFontColor}; '
        if self.saBGColor: html += f'background-color: {self.saBGColor}; '
        html += f'}} .cssSundays{self.cal_ID} {{ '
        if self.dFontFace: html += f'font-family: {self.dFontFace}; '
        if self.dFontSize: html += f'font-size: {self.dFontSize}px; '
        if self.suFontColor: html += f'color: {self.suFontColor}; '
        if self.suBGColor: html += f'background-color: {self.suBGColor}; '
        html += f'}} .cssHilight{self.cal_ID} {{ '
        if self.dFontFace: html += f'font-family: {self.dFontFace}; '
        if self.dFontSize: html += f'font-size: {self.dFontSize}px; '
        if self.dFontColor: html += f'color: {self.dFontColor}; '
        if self.hilightColor: html += f'background-color: {self.hilightColor}; '
        html += 'cursor: default; '
        html += '}} </style>'
        return html

    def leap_year(self, year):
        if year < 1582:
            return year % 4 == 0
        else:
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def get_weekday(self, year, days):
        a = days
        if year: a += (year - 1) * 365
        for i in range(1, year):
            if self.leap_year(i): a += 1
        if year > 1582 or (year == 1582 and days >= 277): a -= 10
        if a: a = (a - self.offset) % 7
        elif self.offset: a += 7 - self.offset
        return a

    def get_week(self, year, days):
        firstWDay = self.get_weekday(year, 0)
        return int(math.floor((days + firstWDay) / 7) + (firstWDay <= 3))

    def table_cell(self, content, cls, date='', style=''):
        size = int(round(self.__size * 1.5))
        html = f'<td align=center width={size} class="{cls}"'

        if content != '&nbsp;' and 'day' in cls.lower():
            link = self.link

            if len(self.specDays) > 0 and content in self.specDays:
                if self.specDays[content][0]:
                    style += f'background-color:{self.specDays[content][0]};'
                if self.specDays[content][1]:
                    html += f' title="{self.specDays[content][1]}"'
                if self.specDays[content][2]:
                    link = self.specDays[content][2]
                    style += 'cursor:pointer;'
                else:
                    link = 'brak'
                    style += 'cursor:pointer;'

            if link == 'brak':
                html += f' onMouseOver="this.className=\'cssHilight{self.cal_ID}\'"'
                html += f' onMouseOut="this.className=\'{cls}\'"'
                html += f' onClick="document.location.href=\'?date={date}\'"'

            if link and link != 'brak':
                html += f' onMouseOver="this.className=\'cssHilight{self.cal_ID}\'"'
                html += f' onMouseOut="this.className=\'{cls}\'"'
                html += f' onClick="document.location.href=\'{link}?date={date}\'"'
        if style: html += f' style="{style}"'
        html += f'>{content}</td>'
        return html

    def table_head(self, content):
        cols = self.weekNumbers and '8' or '7'
        html = f'<tr><td colspan={cols} class="cssTitle{self.cal_ID}" align=center><b>{content}</b></td></tr><tr>'
        if self.weekNumbers: html += '<td></td>'
        for wd in self.weekdays:
            html += f'<td align=center class="cssHeading{self.cal_ID}">{wd}</td>'
        return html + '</tr>'

    def show(self, size=2):
        self.__size = size

        if not (1 <= self.year <= 3999):
            return f'<strong>{self.error[0]}</strong>'
        if not (1 <= self.month <= 12):
            return f'<strong>{self.error[1]}</strong>'

        self.__mDays[1] = 28 + self.leap_year(self.year)
        days = self.__mDays[self.month - 1]

        # Collect holidays
        holidays_set = self.fetch_holidays()

        # Adjust specDays for holidays
        for holiday in holidays_set:
            self.specDays[holiday[0]] = ('#FFDDCC', holiday[1], 'brak')

        # Calendar HTML generation
        html = self.set_styles()
        html += '<table border=0 cellpadding=2 cellspacing=1>'
        html += self.table_head(self.months[self.month - 1] + ' ' + str(self.year))
        wDay = self.get_weekday(self.year, sum(self.__mDays[:self.month - 1]))
        wNum = self.get_week(self.year, sum(self.__mDays[:self.month - 1]) + 1)

        html += '<tr>'
        if self.weekNumbers: html += f'<td align=center class="cssWeeks{self.cal_ID}">{wNum}</td>'
        for i in range(wDay): html += self.table_cell('&nbsp;', f'cssDays{self.cal_ID}')
        for i in range(1, days + 1):
            date = f'{self.year}-{str(self.month).zfill(2)}-{str(i).zfill(2)}'
            cls = 'cssDays{0}'
            if i in self.specDays:
                cls = 'cssHilight{0}'
            elif (wDay + self.offset) % 7 == 0:
                cls = 'cssSaturdays{0}'
            elif (wDay + self.offset) % 7 == 1:
                cls = 'cssSundays{0}'
            html += self.table_cell(i, cls.format(self.cal_ID), date)
            wDay += 1
            if wDay == 7:
                wDay = 0
                wNum += 1
                html += '</tr><tr>'
                if i < days and self.weekNumbers:
                    html += f'<td align=center class="cssWeeks{self.cal_ID}">{wNum}</td>'
        if wDay:
            for i in range(7 - wDay): html += self.table_cell('&nbsp;', f'cssDays{self.cal_ID}')
        html += '</tr></table>'
        return html

    def fetch_holidays(self):
        self.holidays = holidays.RU(years=self.year)
        holiday_set = {(day.day, name) for day, name in self.holidays.items() if day.month == self.month}
        return holiday_set

    def show_week(self, days):
        week_html = self.set_styles()
        week_html += '<table border=0 cellpadding=2 cellspacing=1>'
        week_html += self.table_head('Неделя')

        week_html += '<tr>'
        for day in days:
            day_date = datetime.datetime.strptime(day, '%Y-%m-%d')
            day_num = day_date.day
            weekday = day_date.weekday()

            if weekday == 5:  # Saturday
                cls = 'cssSaturdays{0}'.format(self.cal_ID)
            elif weekday == 6:  # Sunday
                cls = 'cssSundays{0}'.format(self.cal_ID)
            else:
                cls = 'cssDays{0}'.format(self.cal_ID)

            week_html += self.table_cell(day_num, cls, day)
        week_html += '</tr></table>'
        return week_html