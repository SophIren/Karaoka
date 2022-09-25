import pygame
import pygame_gui

from scripts.drawers import PlayDrawer, MainMenuDrawer
from scripts.controllers import PlayController, MainMenuController


class Driver:
    def __init__(self):
        main_menu_drawer = MainMenuDrawer()
        self.main_menu_controller = MainMenuController(
            self, main_menu_drawer)

        play_drawer = PlayDrawer()
        self.play_controller = PlayController(self, play_drawer)

        self.states = {
            "MAIN_MENU": (main_menu_drawer, self.main_menu_controller),
            "PLAY": (play_drawer, self.play_controller)
        }

        self.current_drawer, self.current_controller = None, None
        self.change_state("MAIN_MENU")

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = 60

    def main(self):
        while not self.done:
            time_delta = self.clock.tick(self.fps) / 1000

            self.handle_events()
            self.current_drawer.draw()

            pygame.display.update()
            if self.current_drawer.ui_manager is not None:
                self.current_drawer.ui_manager.update(time_delta)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.current_controller.handle_pressed_button(event)

            if self.current_drawer.ui_manager is not None:
                self.current_drawer.ui_manager.process_events(event)

    def change_state(self, state_name):
        if self.current_controller is not None:
            self.current_controller.deactivate()
        self.current_drawer, self.current_controller = self.states[state_name]
        self.current_controller.activate()

    def start_playing(self, song_audio_path, song_lyrics_path):
        self.play_controller.update_playing_song(song_audio_path,
                                                 song_lyrics_path)
        self.change_state('PLAY')
