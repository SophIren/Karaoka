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
                self.driver.start_playing(
                    os.path.join(self.song_folder_path, selected_song)
                )

        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.refresh_songs()

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
        self.drawer.fit_display()

    def stop_video(self):
        self.video.stop()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['BACK']:
            self.stop_video()
            self.driver.stop_playing()
