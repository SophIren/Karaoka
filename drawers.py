import pygame
import pygame_gui
import moviepy.editor


class IDraw:
    def __init__(self):
        self.ui_manager = None
        self.display = pygame.display.get_surface()
        self.buttons = {}

    def draw(self):
        pass


class PlayDrawer(IDraw):
    def __init__(self):
        super().__init__()
        self.draw()

    def draw(self):
        video = moviepy.editor.VideoFileClip("songs/GiveYouUp.mp4")
        video.preview()


class MainMenuDrawer(IDraw):
    WINDOW_SIZE = (800, 600)

    def __init__(self):
        super().__init__()

        self.display = pygame.display.set_mode(self.WINDOW_SIZE)
        self.ui_manager = pygame_gui.UIManager(self.WINDOW_SIZE,
                                               'GUI/theme.json')
        self.background = pygame.image.load("GUI/bg.jpg")

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
        self.add_song_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 80), (135, 50)),
            text='ADD SONG',
            manager=self.ui_manager,
            container=buttons_layout
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 160), (135, 50)),
            text='EXIT',
            manager=self.ui_manager,
            container=buttons_layout
        )
        self.buttons = {
            'PLAY': self.play_button,
            'ADD_SONG': self.add_song_button,
            'EXIT': self.exit_button
        }

    def draw(self):
        self.display.blit(self.background, (0, 0))
        self.ui_manager.draw_ui(self.display)
