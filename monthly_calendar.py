import math
import time
import holidays

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
        self.offset = 1  # Start the week from Monday
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
        return not (year % 4) and (year < 1582 or year % 100 or not (year % 400))

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
        for i in range(len(self.weekdays)):
            ind = (i + self.offset) % 7 - 1
            wDay = self.weekdays[ind]
            html += self.table_cell(wDay, f'cssHeading{self.cal_ID}')
        if self.weekNumbers: html += self.table_cell('&nbsp;', f'cssHeading{self.cal_ID}')
        html += '</tr>'
        return html

    def view_event(self, start, end, color, title, link=''):
        if start > end: return
        if start < 1 or start > 31: return
        if end < 1 or end > 31: return
        while start <= end:
            self.specDays[str(start)] = [color, title, link]
            start += 1

    def add_holiday(self, day, title):
        if day < 1 or day > 31: return
        self.holidays.append(day)
        self.specDays[str(day)] = ['#D3B58A', title, '']

    def fetch_holidays(self):
        """Fetch public holidays for the specified month and year."""
        try:
            russia_holidays = holidays.RU(years=self.year)
            for date, name in russia_holidays.items():
                if date.month == self.month:
                    self.add_holiday(date.day, name)
        except Exception as e:
            print(f"Error fetching holidays: {e}")

    def create(self):
        self.__size = max(self.hFontSize, self.dFontSize, self.wFontSize)
        date = time.strftime('%Y-%m-%d', time.localtime())
        (curYear, curMonth, curDay) = [int(v) for v in date.split('-')]

        if self.year < 1 or self.year > 3999:
            html = f'<b>{self.error[0]}</b>'
        elif self.month < 1 or self.month > 12:
            html = f'<b>{self.error[1]}</b>'
        else:
            if self.leap_year(self.year):
                self.__mDays[1] = 29
            days = sum(self.__mDays[:self.month - 1])

            start = self.get_weekday(self.year, days)
            stop = self.__mDays[self.month - 1]

            html = self.set_styles()
            html += '<table border=1 cellspacing=0 cellpadding=0><tr>'
            html += f'<td{self.borderColor and f" bgcolor={self.borderColor}"}>'
            html += '<table border=0 cellspacing=1 cellpadding=3>'
            title = f'{self.months[self.month - 1]} {self.year}'
            html += self.table_head(title)
            daycount = 1

            inThisMonth = self.year == curYear and self.month == curMonth

            if self.weekNumbers:
                weekNr = self.get_week(self.year, days)

            while daycount <= stop:
                html += '<tr>'
                wdays = 0

                for i in range(len(self.weekdays)):
                    ind = (i + self.offset) % 7
                    if ind == 6:
                        cls = 'cssSaturdays'
                    elif ind == 0:
                        cls = 'cssSundays'
                    else:
                        cls = 'cssDays'

                    style = ''
                    date = f"{self.year}-{self.month}-{daycount}"

                    if (daycount == 1 and i < start) or daycount > stop:
                        content = '&nbsp;'
                    else:
                        content = str(daycount)
                        if inThisMonth and daycount == curDay:
                            style = f'padding:0px;border:3px solid {self.tdBorderColor};'
                        elif self.year == 1582 and self.month == 10 and daycount == 4:
                            daycount = 14
                        daycount += 1
                        wdays += 1

                    html += self.table_cell(content, f'{cls}{self.cal_ID}', date, style)

                if self.weekNumbers:
                    if not weekNr:
                        if self.year == 1:
                            content = '&nbsp;'
                        elif self.year == 1583:
                            content = '52'
                        else:
                            content = str(self.get_week(self.year - 1, 365))
                    elif self.month == 12 and weekNr >= 52 and wdays < 4:
                        content = '1'
                    else:
                        content = str(weekNr)

                    html += self.table_cell(content, f'cssWeeks{self.cal_ID}')
                    weekNr += 1

                html += '</tr>'
            html += '</table></td></tr></table>'
        return html
