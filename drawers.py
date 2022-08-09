import pygame
import pygame_gui


class IDraw:
    def __init__(self):
        self.ui_manager = None
        self.display = pygame.display.get_surface()
        self.update_ui_manager()
        self.buttons = {}

    def update_ui_manager(self):
        self.ui_manager = pygame_gui.UIManager(pygame.display.get_window_size(),
                                               'GUI/theme.json')

    def draw(self):
        pass

    def fit_display(self):
        self.update_ui_manager()


class PlayDrawer(IDraw):
    def __init__(self):
        super().__init__()

        self.video = None
        self.back_button = None

    def fit_display(self):
        x_size, y_size = self.video.get_size()

        pygame.display.set_mode((x_size, y_size))
        self.update_ui_manager()

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_size - 135, y_size - 50), (135, 50)),
            text='BACK',
            manager=self.ui_manager)
        self.buttons['BACK'] = self.back_button

    def update_playing_song(self, video):
        self.video = video
        # self.video.set_size(self.display.get_size())

    def draw(self):
        self.video.draw_to(self.display, (0, 0))
        self.ui_manager.draw_ui(self.display)


class MainMenuDrawer(IDraw):
    def __init__(self):
        super().__init__()

        self.background = pygame.image.load("GUI/bg.jpg")
        pygame.display.set_mode(self.background.get_size())

        self.song_selector = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((100, 100), (200, 100)),
            item_list=[],
            manager=self.ui_manager
        )

        self.play_button = None
        self.refresh_button = None
        self.init_buttons()

    def init_buttons(self):
        buttons_layout = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((480, 180), (135, 220)),
            manager=self.ui_manager
        )
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (135, 50)),
            text='PLAY',
            manager=self.ui_manager,
            container=buttons_layout)
        self.refresh_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 80), (135, 50)),
            text='REFRESH',
            manager=self.ui_manager,
            container=buttons_layout
        )
        self.buttons['PLAY'] = self.play_button
        self.buttons['REFRESH'] = self.refresh_button

    def fit_display(self):
        pygame.display.set_mode(self.background.get_size())

    def update_song_selector(self, song_names):
        self.song_selector.set_item_list(song_names)

    def draw(self):
        self.display.blit(self.background, (0, 0))
        self.ui_manager.draw_ui(self.display)
