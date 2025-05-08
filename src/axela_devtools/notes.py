from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Note:
    name:str
    text:str
    created_at: date
    category: Optional[str]
    location: str


class Notepad(ABC):
    # TODO some link between main search and searches
    @abstractmethod
    def search_note(self):
        pass

    @abstractmethod
    def search_note_by_name(self,name:str):
        pass

    @abstractmethod
    def search_note_by_date(self, note_date: date):
        pass

    @abstractmethod
    def search_note_by_category(self, category: str):
        pass

    @abstractmethod
    def create_note(self, text:str, name:str, category:Optional[str]):
        pass

    @abstractmethod
    def delete_note(self, note: Note):
        pass

    @abstractmethod
    def extend_note(self, note: Note):
        pass

    @abstractmethod
    def overwrite_note(self,note: Note):
        pass

