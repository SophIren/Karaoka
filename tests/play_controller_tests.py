import pytest

from scripts.controllers import PlayController


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


def test_play_controller_activate(play_controller, mocked_lt_parser):
    play_controller.activate()

    assert isinstance(play_controller.lt_parser, mocked_lt_parser)
    assert play_controller.media_player.is_playing
    assert play_controller.recorder.is_recording


def test_play_controller_tick(play_controller):
    play_controller.tick()

    assert play_controller.lt_parser.time_actualized
    assert play_controller.lt_parser.lines_gotten
    assert play_controller.drawer.activated
    assert play_controller.drawer.drawn


def test_play_controller_deactivate(play_controller):
    play_controller.deactivate()

    assert not play_controller.media_player.is_playing
    assert play_controller.recorder.saved
    assert not play_controller.recorder.is_recording


def test_update_chosen_song(play_controller):
    play_controller.update_chosen_song('lol', 'kek')

    assert play_controller.audio_path == 'lol'
    assert play_controller.lyrics_path == 'kek'
    assert play_controller.media_player.media_set
