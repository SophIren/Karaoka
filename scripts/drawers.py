import pygame
import pygame_gui


class IDraw:
    GUI_THEME_PATH = 'GUI/theme.json'

    def __init__(self):
        self.ui_manager = None
        self.display = pygame.display.get_surface()
        self.update_ui_manager()
        self.buttons = {}

    def update_ui_manager(self):
        self.ui_manager = pygame_gui.UIManager(pygame.display.get_window_size(),
                                               self.GUI_THEME_PATH)

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
    BACKGROUND_PATH = 'GUI/bg.jpg'

    def __init__(self):
        super().__init__()

        self.background = pygame.image.load(self.BACKGROUND_PATH)
        pygame.display.set_mode(self.background.get_size())
        self.update_ui_manager()

        self.general_layout = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((450, 100, 400, 550)),
            manager=self.ui_manager
        )

        self.play_button = None
        self.refresh_button = None
        self.song_selector = None
        self.init_song_selector()
        self.init_buttons()

    def init_song_selector(self):
        song_selector_rect = pygame.Rect((0, 0), (400, 500))
        song_selector_rect.bottomleft = (0, 0)
        self.song_selector = pygame_gui.elements.UISelectionList(
            relative_rect=song_selector_rect,
            item_list=[],
            manager=self.ui_manager,
            container=self.general_layout,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'bottom',
                'bottom': 'bottom'
            }
        )

    def init_buttons(self):
        play_button_rect = pygame.Rect(0, 0, 135, 50)
        play_button_rect.topright = (0, 0)
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=play_button_rect,
            text='PLAY',
            manager=self.ui_manager,
            container=self.general_layout,
            anchors={
                'left': 'right',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        self.refresh_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (135, 50)),
            text='REFRESH',
            manager=self.ui_manager,
            container=self.general_layout,
        )

        self.buttons['PLAY'] = self.play_button
        self.buttons['REFRESH'] = self.refresh_button

    def fit_display(self):
        pygame.display.set_mode(self.background.get_size())

    def update_song_selector(self, song_names):
        self.song_selector.set_dimensions(
            (400, min(500, len(song_names) * 35 + 6)))
        self.song_selector.set_item_list(song_names)

    def draw(self):
        self.display.blit(self.background, (0, 0))
        self.ui_manager.draw_ui(self.display)
