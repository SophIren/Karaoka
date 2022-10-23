import pytest

from scripts.driver import Driver


@pytest.fixture(autouse=True)
def init(mocker, mocked_controller):
    mocker.patch('scripts.driver.MainMenuController', mocked_controller)
    mocker.patch('scripts.driver.PlayController', mocked_controller)
    mocker.patch('scripts.driver.MainMenuDrawer', lambda: 'MMDrawer')
    mocker.patch('scripts.driver.PlayDrawer', lambda: 'PlayDrawer')


@pytest.mark.parametrize('state_name',
                         ['MAIN_MENU', 'PLAY'])
def test_change_state(state_name):
    driver = Driver()
    driver.change_state(state_name)

    assert_state_changed(driver, state_name)


def test_menu_to_playing_transfer():
    driver = Driver()
    driver.menu_to_playing_transfer('lol', 'kek')

    assert_state_changed(driver, 'PLAY')
    assert driver.play_controller.song_audio_path == 'lol'
    assert driver.play_controller.song_lyrics_path == 'kek'


def assert_state_changed(driver, state_name):
    assert driver.current_controller == driver.states[state_name]
    assert driver.current_controller.activated
