import glob
import os.path
import mimetypes
from pathlib import Path
from ffpyplayer.player import MediaPlayer

from scripts.recording import Recorder


class IController:
    def __init__(self, driver, drawer):
        self.driver = driver
        self.drawer = drawer

    def handle_pressed_button(self, event):
        pass

    def activate(self):
        self.drawer.activate()

    def deactivate(self):
        pass


class MainMenuController(IController):
    SONG_MEDIA_FOLDER_PATH = 'songs/media/'
    SONG_LYRICS_FOLDER_PATH = 'songs/lyrics/'

    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['PLAY']:
            self.start_playing()

        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.refresh_songs()

    @staticmethod
    def is_correct_media_file(file_name):
        if file_name is None:
            return False
        file_type = mimetypes.guess_type(file_name)[0].split('/')[0]
        return file_type == 'audio' or file_type == 'video'

    @staticmethod
    def lyrics_file_exists(file_name):
        return Path(
            os.path.join(MainMenuController.SONG_LYRICS_FOLDER_PATH, file_name)
        ).is_file()

    def start_playing(self):
        song_audio_name = self.drawer.song_selector.get_single_selection()
        if not self.is_correct_media_file(song_audio_name):
            return

        song_lyrics_name = os.path.splitext(song_audio_name)[0] + '.lt'
        if not self.lyrics_file_exists(song_lyrics_name):
            return

        self.driver.start_playing(
            os.path.join(self.SONG_MEDIA_FOLDER_PATH, song_audio_name),
            os.path.join(self.SONG_LYRICS_FOLDER_PATH, song_lyrics_name)
        )

    def activate(self):
        super(MainMenuController, self).activate()
        self.refresh_songs()

    def refresh_songs(self):
        song_names = list(map(os.path.basename,
                              glob.glob(self.SONG_MEDIA_FOLDER_PATH + '/*')))
        self.drawer.update_song_selector(song_names)


class PlayController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.audio_path = None
        self.lyrics_file = None
        self.media_player = None
        self.recorder = Recorder()

    def update_playing_song(self, audio_path, lyrics_path):
        self.audio_path = audio_path
        self.lyrics_file = open(lyrics_path, encoding='utf-8')

    def activate(self):
        super(PlayController, self).activate()
        self.media_player = MediaPlayer(self.audio_path)
        self.recorder.start_recording()

    def deactivate(self):
        self.media_player.close_player()
        self.recorder.save_overlapped()
        self.recorder.stop_recording()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['BACK']:
            self.driver.change_state("MAIN_MENU")
