from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEvent:
    name:str
    start_time:datetime
    end_time:datetime

class CalendarManager(ABC):

    @abstractmethod
    def get_current_date_and_time(self):
        pass

    @abstractmethod
    def add_to_calendar(self):
        pass

    @abstractmethod
    def edit_event(self, event: CalendarEvent):
        pass

    @abstractmethod
    def delete_event(self, event: CalendarEvent):
        pass

    @abstractmethod
    def count_time_to_event(self, event: CalendarEvent):
        pass

    @abstractmethod
    def set_alarm(self):
        pass

    @abstractmethod
    def delete_alarm(self):
        pass

    @abstractmethod
    def week_summary(self):
        pass

    @abstractmethod
    def day_summary(self):
        pass
