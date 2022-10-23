import pytest

from scripts.controllers import PlayController, MainMenuController


@pytest.fixture(autouse=True)
def init(mocker, mocked_lt_parser, mocked_recorder):
    mocker.patch('scripts.controllers.LTParser', mocked_lt_parser)
    mocker.patch('scripts.controllers.Recorder', mocked_recorder)


@pytest.fixture()
def play_controller(mocked_driver, mocked_drawer, mocked_media_player):
    play_controller = PlayController(mocked_driver(), mocked_drawer())
    play_controller.media_player = mocked_media_player()
    play_controller.activate()

    return play_controller


@pytest.fixture()
def main_menu_controller(mocked_driver, mocked_drawer):
    MainMenuController.SONG_MEDIA_FOLDER_PATH = ''
    MainMenuController.SONG_LYRICS_FOLDER_PATH = ''

    main_menu_controller = MainMenuController(mocked_driver(), mocked_drawer())
    main_menu_controller.activate()

    return main_menu_controller
