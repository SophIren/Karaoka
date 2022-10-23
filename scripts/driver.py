import pygame

from scripts.controllers import PlayController, MainMenuController
from scripts.drawers import PlayDrawer, MainMenuDrawer


class Driver:
    def __init__(self):
        main_menu_drawer = MainMenuDrawer()
        self.main_menu_controller = MainMenuController(self, main_menu_drawer)

        play_drawer = PlayDrawer()
        self.play_controller = PlayController(self, play_drawer)

        self.states = {
            "MAIN_MENU": self.main_menu_controller,
            "PLAY": self.play_controller
        }

        self.current_controller = None
        self.change_state("MAIN_MENU")

        self.done = False

    def main(self):
        while not self.done:
            self.handle_events()
            self.current_controller.tick()

            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            self.current_controller.handle_event(event)

    def change_state(self, state_name):
        if self.current_controller is not None:
            self.current_controller.deactivate()
        self.current_controller = self.states[state_name]
        self.current_controller.activate()

    def menu_to_playing_transfer(self, song_audio_path, song_lyrics_path):
        self.play_controller.update_chosen_song(song_audio_path,
                                                song_lyrics_path)
        self.change_state('PLAY')
