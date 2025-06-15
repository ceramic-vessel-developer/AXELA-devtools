from datetime import date
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(__file__))

from notes import Notepad, Note

CLASS_NAME = "DummyNotepad"

class DummyNotepad(Notepad):
    def search_note(self):
        print("search_note wywołane")

    def search_note_by_name(self, name: str):
        print(f"search_note_by_name wywołane z: {name}")

    def search_note_by_date(self, note_date: date):
        print(f"search_note_by_date wywołane z: {note_date}")

    def search_note_by_category(self, category: str):
        print(f"search_note_by_category wywołane z: {category}")

    def create_note(self, text: str, name: str, category: Optional[str]):
        print(f"create_note wywołane z: text='{text}', name='{name}', category='{category}'")

    def delete_note(self, note: Note):
        print(f"delete_note wywołane z: {note}")

    def extend_note(self, note: Note):
        print(f"extend_note wywołane z: {note}")

    def overwrite_note(self, note: Note):
        print(f"overwrite_note wywołane z: {note}")
