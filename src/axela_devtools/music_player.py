from enum import Enum
from abc import ABC, abstractmethod

CLASS_NAME = "Player"

class LoopTypes(Enum):
    NONE = "NONE"
    ONE_SONG = "ONE_SONG"
    PLAYLIST = "PLAYLIST"


class Player(ABC):

    @abstractmethod
    def configure_hardware(self):
        pass

    @abstractmethod
    def play_song(self, name:str):
        pass

    @abstractmethod
    def play_playlist(self, playlist_name: str):
        pass

    @abstractmethod
    def volume_up(self):
        pass

    @abstractmethod
    def volume_down(self):
        pass

    @abstractmethod
    def next_song(self):
        pass

    @abstractmethod
    def previous_song(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def loop(self, loop_type: LoopTypes):
        pass
