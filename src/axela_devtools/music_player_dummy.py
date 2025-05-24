import sys
import os

sys.path.append(os.path.dirname(__file__))

from music_player import Player, LoopTypes

CLASS_NAME = "DummyMusicPlayer"

class DummyMusicPlayer(Player):
    def configure_hardware(self):
        print("funkcja configure_hardware")

    def play_song(self, name: str):
        print(f"funkcja play_song: {name}")

    def play_playlist(self, playlist_name: str):
        print(f"funkcja play_playlist: {playlist_name}")

    def volume_up(self):
        print("funkcja volume_up")

    def volume_down(self):
        print("funkcja volume_down")

    def next_song(self):
        print("funkcja next_song")

    def previous_song(self):
        print("funkcja previous_song")

    def pause(self):
        print("funkcja pause")

    def play(self):
        print("funkcja play")

    def loop(self, loop_type: LoopTypes):
        print(f"funkcja loop: {loop_type}")
