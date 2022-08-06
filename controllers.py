class IController:
    def __init__(self, driver, drawer):
        self.driver = driver
        self.drawer = drawer

    def handle_pressed_button(self, event):
        pass


class MainMenuController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)

    def handle_pressed_button(self, event):
        if event.ui_element == self.drawer.buttons['EXIT']:
            self.driver.done = True
        if event.ui_element == self.drawer.buttons['PLAY']:
            self.driver.change_state('PLAY')


class PlayController(IController):
    def __init__(self, driver, drawer):
        super().__init__(driver, drawer)

    def handle_pressed_button(self, event):
        pass
