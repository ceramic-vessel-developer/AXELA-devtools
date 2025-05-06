from abc import ABC, abstractmethod

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

    # TODO change string to enum
    @abstractmethod
    def loop(self, loop_type: str):
        pass
