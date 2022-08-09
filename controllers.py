import glob
import os.path

from pygamevideo import Video


class IController:
    def __init__(self, driver, drawer):
        self.driver = driver
        self.drawer = drawer

    def handle_pressed_button(self, event):
        pass


class MainMenuController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.song_folder_path = None
        self.refresh_songs()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['EXIT']:
            self.driver.done = True

        if event.ui_element == self.drawer.buttons['PLAY']:
            play_controller = self.driver.states['PLAY'][1]
            play_controller.update_playing_song(
                os.path.join(self.song_folder_path,
                             self.drawer.song_selector.get_single_selection())
            )
            play_controller.play_video()
            self.driver.change_state('PLAY')

        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.refresh_songs()

    def refresh_songs(self, path='songs/'):
        self.song_folder_path = path

        song_names = list(map(os.path.basename, glob.glob(path + '/*')))
        self.drawer.update_song_selector(song_names)


class PlayController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.video = None

    def update_playing_song(self, path):
        self.video = Video(path)
        self.drawer.update_playing_song(self.video)

    def play_video(self):
        self.video.play()

    def handle_pressed_button(self, event):
        pass
