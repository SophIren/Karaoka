import pygame
import pygame_gui

from drawers import PlayDrawer, MainMenuDrawer
from controllers import PlayController, MainMenuController


class Driver:
    def __init__(self):
        main_menu_drawer = MainMenuDrawer()
        self.main_menu_controller = MainMenuController(self,
                                                       main_menu_drawer)

        play_drawer = PlayDrawer()
        self.play_controller = PlayController(self, play_drawer)

        self.states = {
            "MAIN_MENU": (main_menu_drawer, self.main_menu_controller),
            "PLAY": (play_drawer, self.play_controller)
        }
        self.current_state_name = "MAIN_MENU"
        self.current_drawer, self.current_controller = \
            self.states[self.current_state_name]
        self.current_ui_manager = self.current_drawer.ui_manager

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = 60

    def main(self):
        while not self.done:
            time_delta = self.clock.tick(self.fps) / 1000

            self.handle_events()
            self.current_drawer.draw()

            pygame.display.update()
            if self.current_ui_manager is not None:
                self.current_ui_manager.update(time_delta)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.current_controller.handle_pressed_button(event)

            if self.current_ui_manager is not None:
                self.current_ui_manager.process_events(event)

    def change_state(self, state_name):
        self.current_state_name = state_name
        self.current_drawer, self.current_controller = \
            self.states[self.current_state_name]
        self.current_ui_manager = self.current_drawer.ui_manager

    def start_playing(self, song_path):
        try:
            self.play_controller.update_playing_song(song_path)
            self.play_controller.play_video()
            self.play_controller.record_audio()
            self.change_state('PLAY')
        except ZeroDivisionError:  # Invalid file
            pass

    def stop_playing(self):
        self.change_state('MAIN_MENU')
        self.main_menu_controller.drawer.fit_display()
