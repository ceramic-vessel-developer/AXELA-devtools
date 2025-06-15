from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(__file__))
from our_calendar import CalendarManager, CalendarEvent

CLASS_NAME = "DummyCalendarManager"

class DummyCalendarManager(CalendarManager):
    def get_current_date_and_time(self):
        print("get_current_date_and_time wywołane")
        return datetime.now()

    def add_to_calendar(self):
        print("add_to_calendar wywołane")

    def edit_event(self, event: CalendarEvent):
        print(f"edit_event wywołane z: {event}")

    def delete_event(self, event: CalendarEvent):
        print(f"delete_event wywołane z: {event}")

    def count_time_to_event(self, event: CalendarEvent):
        print(f"count_time_to_event wywołane z: {event}")

    def set_alarm(self):
        print("set_alarm wywołane")

    def delete_alarm(self):
        print("delete_alarm wywołane")

    def week_summary(self):
        print("week_summary wywołane")

    def day_summary(self):
        print("day_summary wywołane")
