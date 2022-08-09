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
        self.song_folder_path = 'songs/'
        self.refresh_songs()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['PLAY']:
            selected_song = self.drawer.song_selector.get_single_selection()
            if selected_song is not None:
                self.start_playing()

        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.refresh_songs()

    def start_playing(self):
        play_controller = self.driver.states['PLAY'][1]
        play_controller.update_playing_song(
            os.path.join(self.song_folder_path,
                         self.drawer.song_selector.get_single_selection())
        )
        play_controller.play_video()
        self.driver.change_state('PLAY')

    def refresh_songs(self):
        song_names = list(map(os.path.basename,
                              glob.glob(self.song_folder_path + '/*')))
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
        self.fit_display_to_video()

    def fit_display_to_video(self):
        self.drawer.fit_display_to_video()

    def handle_pressed_button(self, event):
        pass
