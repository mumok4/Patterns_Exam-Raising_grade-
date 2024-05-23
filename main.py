import  datetime
from monthly_calendar import MonthlyCalendar


class CalendarHTML:
    def __init__(self):
        self.monthly_calendar = MonthlyCalendar()

    def generate_yearly_calendar(self, year):
        months_html = []
        for month in range(1, 13):
            self.monthly_calendar = MonthlyCalendar(year, month)
            months_html.append(self.monthly_calendar.show())
        return "<br>".join(months_html)

    def generate_monthly_calendar(self, year, month):
        self.monthly_calendar = MonthlyCalendar(year, month)
        return self.monthly_calendar.show()

    def generate_weekly_calendar(self, year, week):
        # Определяем первый день года
        first_day_of_year = datetime.date(year, 1, 1)
        # Определяем день начала первой недели (ISO 8601)
        first_week_day = first_day_of_year - datetime.timedelta(days=first_day_of_year.isoweekday() - 1)
        # Определяем первый день искомой недели
        first_day_of_week = first_week_day + datetime.timedelta(weeks=week-1)
        # Собираем все дни недели
        days = [(first_day_of_week + datetime.timedelta(days=i)).isoformat() for i in range(7)]
        return self.monthly_calendar.show_week(days)

    def generate_calendar(self, year, month=None, day=None):
        if month is None:
            # Generate yearly calendar
            html_content = self.generate_yearly_calendar(year)
            filename = f'calendar_{year}.html'
        elif day is None:
            # Generate monthly calendar
            html_content = self.generate_monthly_calendar(year, month)
            filename = f'calendar_{year}_{str(month).zfill(2)}.html'
        else:
            # Generate weekly calendar
            week = datetime.date(year, month, day).isocalendar()[1]
            html_content = self.generate_weekly_calendar(year, week)
            filename = f'calendar_{year}_{str(month).zfill(2)}_{str(day).zfill(2)}.html'

        # Save to file
        with open(filename, 'w', encoding='cp1251') as f:
            f.write(html_content)

        return filename


calendar_html = CalendarHTML()
calendar_html.generate_calendar(2024)  # Yearly calendar
calendar_html.generate_calendar(2024, 5) # Monthly calendar
calendar_html.generate_calendar(2024, 5, 1)  # Weekly calendar
