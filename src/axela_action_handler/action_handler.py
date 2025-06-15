import importlib.util
import os
from pathlib import Path
from datetime import date
import threading
import time
import sounddevice as sd
import soundfile as sf
import keyboard

from axela_devtools.music_player import LoopTypes
from axela_devtools.notes import Note
import tts
import speech_to_text


class AxelaActionHandler:

    def __init__(self, modules):
        self.music_player_module = self.load_module(modules['music_player_path'], 'music_module')
        self.monitoring_module = self.load_module(modules['monitoring_path'], 'monitoring_module')
        self.calendar_module = self.load_module(modules['calendar_path'], 'calendar_module')
        self.notes_module = self.load_module(modules['notes_path'], 'notes_module')
        self.current_command = "Axela volume up by 80"
        self.device_microphone = None
        self._stop_event = threading.Event()
        self._listener_thread = threading.Thread(target=self._background_listener, daemon=True)
        self._listener_thread.start()

        self.note_key_phrases = {
            "search note": 2, "search note by name": 4, "search note by date": 4, "search note by category": 4,
            "create note": 2, "delete note": 2, "extend note": 2, "overwrite note": 2
        }
        self.music_key_phrases = {
            "configure hardware": 2, "play song": 2, "play playlist": 2, "volume up": 2, "volume down": 2,
            "next song": 2, "previous song": 2, "pause": 1, "play": 1, "loop": 1
        }
        self.monitoring_key_phrases = {
            "check darkness level": 3, "check camera status": 3, "check outdoor": 2
        }
        self.calendar_key_phrases = {
            "get current date and time": 5, "add to calendar": 3, "edit event": 2, "delete event": 2,
            "count time to event": 4,
            "set alarm": 2, "delete alarm": 2, "week summary": 2, "day summary": 2
        }

    def load_module(self, module_path, module_name):

        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Module path '{module_path}' not found.")

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec from {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, 'CLASS_NAME'):
            raise AttributeError(f"Module '{module_name}' must define a CLASS_NAME variable.")

        class_name = getattr(module, 'CLASS_NAME')

        if not hasattr(module, class_name):
            raise AttributeError(f"Class '{class_name}' not found in module '{module_name}'.")

        class_instance = getattr(module, class_name)
        return class_instance()

    def search_keyword(self, text: str):

        lowered_text = text.lower()
        if "axela" not in lowered_text:
            return "Please try again"

        words = lowered_text.split()
        try:
            index = words.index("axela")
            after_axela = words[index + 1:]

            categories = {
                "notes": self.note_key_phrases,
                "music": self.music_key_phrases,
                "monitoring": self.monitoring_key_phrases,
                "calendar": self.calendar_key_phrases
            }

            for category, phrases in categories.items():
                for phrase, word_count in phrases.items():
                    phrase_words = phrase.split()
                    if after_axela[:word_count] == phrase_words:
                        remaining_text = ' '.join(after_axela[word_count:])
                        return self.keyword_handler(category, phrase, remaining_text)

        except ValueError:
            return "Please try again"

    def keyword_handler(self, category: str, keyphrase: str, content: str):
        keyphrase = keyphrase.replace(" ", "_")
        print(f"Matched category: {category}")
        print(f"Matched keyphrase: {keyphrase}")
        print(f"Command content: {content}")

        if category == "notes":
            return self.handle_notes(keyphrase, content)
        elif category == "music":
            return self.handle_music(keyphrase, content)
        elif category == "monitoring":
            return self.handle_monitoring(keyphrase, content)
        elif category == "calendar":
            return self.handle_calendar(keyphrase, content)
        else:
            return "Please try again"

    def handle_notes(self, keyphrase: str, content: str):
        print(f"Notes - Keyphrase: '{keyphrase}', Content: '{content}'")
        func = getattr(self.notes_module, keyphrase)

        def search_note():
            return func()

        def search_note_by_name():
            return func(name=content)

        def search_note_by_date():
            day_str = content[0]
            month_str = content[1]
            year_str = content[2]

            months_map = {
                "january": 1, "february": 2, "march": 3, "april": 4,
                "may": 5, "june": 6, "july": 7, "august": 8,
                "september": 9, "october": 10, "november": 11, "december": 12
            }

            day = int(day_str)
            month = months_map.get(month_str)
            year = int(year_str)

            if month is None:
                raise ValueError(f"Unknown month name: {month_str}")

            note_date = date(year, month, day)

            return func(note_date)

        def search_note_by_category():
            return func(category=content)

        def create_note():
            if content[1] == 'category':
                category = content[2]
                return func(name=content[0], text=content[3:], category=category)
            else:
                return func(name=content[0], text=content[1:])

        def delete_note():
            note_to_delete = search_note_by_name()
            return func(note=note_to_delete)

        def extend_note():
            note_to_extend = search_note_by_name()
            return func(note=note_to_extend)

        def overwrite_note():
            is_note_deleted = delete_note()
            if is_note_deleted:
                return create_note()

        function_map = {
            "search_note": search_note,
            "search_note_by_name": search_note_by_name,
            "search_note_by_date": search_note_by_date,
            "search_note_by_category": search_note_by_category,
            "create_note": create_note,
            "delete_note": delete_note,
            "extend_note": extend_note,
            "overwrite_note": overwrite_note,
        }
        if keyphrase in function_map:
            function_to_perform = function_map.get(keyphrase)
            function_to_perform()

    def handle_music(self, keyphrase: str, content: str):
        print(f"Music - Keyphrase: '{keyphrase}', Content: '{content}'")
        func = getattr(self.music_player_module, keyphrase)

        def configure_hardware():
            return func()

        def play_song():
            return func(name=content)

        def play_playlist():
            return func(playlist_name=content)

        def volume_up():
            return func()

        def volume_down():
            return func()

        def next_song():
            return func()

        def previous_song():
            return func()

        def pause():
            return func()

        def play():
            return func()

        def loop():
            if "playlist" in content:
                return func(LoopTypes.PLAYLIST)
            elif "song" in content:
                return func(LoopTypes.ONE_SONG)
            else:
                return func(LoopTypes.NONE)

        function_map = {
            "configure_hardware": configure_hardware,
            "play_song": play_song,
            "play_playlist": play_playlist,
            "volume_up": volume_up,
            "volume_down": volume_down,
            "next_song": next_song,
            "previous_song": previous_song,
            "pause": pause,
            "play": play,
            "loop": loop,
        }
        if keyphrase in function_map:
            function_to_perform = function_map.get(keyphrase)
            function_to_perform()

    def receive_command(self):
        if self.current_command == "":
            self.current_command = speech_to_text.speech_to_text(".\\command.wav")

    def _background_listener(self):
        not_ready_flag = True
        while not self._stop_event.is_set():
            if not_ready_flag and not keyboard.is_pressed("enter"):
                not_ready_flag = False
                threading.Thread(target=self._space_record_listener, daemon=True).start()
            if self.current_command != "":
                print(f"\n[Thread] Received command: {self.current_command}")
                result = self.search_keyword(self.current_command)
                self.current_command = ""
                tts.tts(result, 'en', 'response')
            time.sleep(0.25)

    def _space_record_listener(self):
        print("[RecordingListener] recording key listener started.")
        self.device_microphone = sd.default.device[0]  # przypisanie domyślnego mikrofonu
        samplerate = 44100
        channels = 1
        recording = []
        is_recording = False
        stream = None

        while not self._stop_event.is_set():
            if keyboard.is_pressed("space") and not is_recording:
                print("[RecordingListener] Space pressed - start recording")
                recording = []
                is_recording = True
                stream = sd.InputStream(
                    samplerate=samplerate,
                    channels=channels,
                    callback=lambda indata, frames, time_info, status: recording.extend(indata.copy())
                )
                stream.start()

            elif not keyboard.is_pressed("space") and is_recording:
                print("[RecordingListener] Space released - stop recording.")
                stream.stop()
                stream.close()
                is_recording = False

                file_path = "command.wav"
                sf.write(file_path, recording, samplerate)
                print(f"[Listener] Audio saved to {file_path}")

                self.receive_command()

            time.sleep(0.05)

    def handle_monitoring(self, keyphrase: str, content: str):
        print(f"Monitoring - Keyphrase: '{keyphrase}', Content: '{content}'")
        func = getattr(self.monitoring_module, keyphrase)

        def check_darkness_level():
            return func()

        def check_camera_status():
            return func()

        def check_outdoor():
            return func()

        function_map = {
            "check_darkness_level": check_darkness_level,
            "check_camera_status": check_camera_status,
            "check_outdoor": check_outdoor
        }

        if keyphrase in function_map:
            function_to_perform = function_map.get(keyphrase)
            function_to_perform()

    def handle_calendar(self, keyphrase: str, content: str):
        print(f"Calendar - Keyphrase: '{keyphrase}', Content: '{content}'")
        func = getattr(self.calendar_module, keyphrase)

        def get_current_date_and_time():
            return func()

        def add_to_calendar():
            return func()

        def edit_event():
            return func()

        def delete_event():
            return func()

        def count_time_to_event():
            return func()

        def set_alarm():
            return func()

        def delete_alarm():
            return func()

        def week_summary():
            return func()

        def day_summary():
            return func()

        function_map = {
            "get_current_date_and_time": get_current_date_and_time,
            "add_to_calendar": add_to_calendar,
            "edit_event": edit_event,
            "delete_event": delete_event,
            "count_time_to_event": count_time_to_event,
            "set_alarm": set_alarm,
            "delete_alarm": delete_alarm,
            "week_summary": week_summary,
            "day_summary": day_summary,
        }

        if keyphrase in function_map:
            function_to_perform = function_map.get(keyphrase)
            function_to_perform()


current_file = Path(__file__).resolve()
parent_dir = current_file.parent.parent

modules_paths = {
    'music_player_path': str(parent_dir / "axela_devtools" / "music_player_dummy.py"),
    'monitoring_path': str(parent_dir / "axela_devtools" / "monitoring_dummy.py"),
    'calendar_path': str(parent_dir / "axela_devtools" / "calendar_dummy.py"),
    'notes_path': str(parent_dir / "axela_devtools" / "notes_dummy.py"),
}

testing = AxelaActionHandler(modules_paths)

while True:
    pass
