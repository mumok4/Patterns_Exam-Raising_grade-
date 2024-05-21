from monthly_calendar import MonthlyCalendar

class CalendarSingleton:
    _instances = {
        "monthly": None,
        "weekly": None,
        "yearly": None
    }

    @staticmethod
    def get_instance(calendar_type="monthly", year=None, month=None, day=None):
        if calendar_type not in CalendarSingleton._instances:
            raise ValueError("Unknown calendar type")

        if CalendarSingleton._instances[calendar_type] is None:
            if calendar_type == "monthly":
                CalendarSingleton._instances[calendar_type] = MonthlyCalendar(year, month)
            elif calendar_type == "weekly":
                pass
            elif calendar_type == "yearly":
                pass

        return CalendarSingleton._instances[calendar_type]

class CalendarFactory:
    @staticmethod
    def create_calendar(calendar_type="monthly", year=None, month=None, day=None):
        if calendar_type == "monthly":
            return MonthlyCalendar(year, month)
        elif calendar_type == "weekly":
            pass
        elif calendar_type == "yearly":
            pass
        else:
            raise ValueError("Unknown calendar type")

if __name__ == "__main__":
    filepath = "calendar_month.html"
    calendar = CalendarFactory.create_calendar("monthly")
    body = calendar.create()
    html = f"<!DOCTYPE html><html><body>{body}</body></html>"
    with open(filepath, "w") as file:
        file.write(html)