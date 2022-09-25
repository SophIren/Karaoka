import glob
import os.path

from scripts.playing import VideoPlayer
from scripts.recording import Recorder


class IController:
    def __init__(self, driver, drawer):
        self.driver = driver
        self.drawer = drawer

    def handle_pressed_button(self, event):
        pass


class MainMenuController(IController):
    SONG_FOLDER_PATH = 'songs/'

    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.refresh_songs()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['PLAY']:
            selected_song = self.drawer.song_selector.get_single_selection()
            if selected_song is not None:
                self.driver.start_playing(
                    os.path.join(self.SONG_FOLDER_PATH, selected_song)
                )

        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.refresh_songs()

    def refresh_songs(self):
        song_names = list(map(os.path.basename,
                              glob.glob(self.SONG_FOLDER_PATH + '/*')))
        self.drawer.update_song_selector(song_names)


class PlayController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.video = None
        self.recorder = Recorder()

    def update_playing_song(self, path):
        self.video = VideoPlayer(path)
        self.drawer.update_playing_song(self.video)

    def play_video(self):
        self.video.play()
        self.drawer.fit_display()

    def record_audio(self):
        self.recorder.start_recording()

    def stop_video(self):
        self.video.stop()

    def stop_recording(self):
        self.recorder.stop_recording()
        self.recorder.save_recorded_frames()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['BACK']:
            self.stop_video()
            self.stop_recording()
            self.driver.stop_playing()
