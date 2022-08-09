import glob
import os.path


class IController:
    def __init__(self, driver, drawer):
        self.driver = driver
        self.drawer = drawer

    def handle_pressed_button(self, event):
        pass


class MainMenuController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)
        self.update_songs()

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['EXIT']:
            self.driver.done = True
        if event.ui_element == self.drawer.buttons['PLAY']:
            self.driver.change_state('PLAY')
        if event.ui_element == self.drawer.buttons['REFRESH']:
            self.update_songs()

    def update_songs(self, path='songs'):
        song_names = list(map(os.path.basename, glob.glob(path + '/*')))
        self.drawer.update_song_selector(song_names)


class PlayController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)

    def handle_pressed_button(self, event):
        pass
