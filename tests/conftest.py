import pytest


@pytest.fixture()
def mocked_drawer():
    class MockedDrawer:
        def __init__(self):
            self.drawn = False
            self.activated = False
            self.ui_manager = None

        def draw(self, *args):
            self.drawn = True

        def activate(self):
            self.activated = True

    return MockedDrawer


@pytest.fixture()
def mocked_driver():
    class MockedDriver:
        def __init__(self):
            pass

    return MockedDriver


@pytest.fixture()
def mocked_media_player():
    class MockedMediaPlayer:
        def __init__(self):
            self.is_playing = False
            self.media_set = False

        def play(self):
            self.is_playing = True

        def stop(self):
            self.is_playing = False

        def set_media(self, media):
            self.media_set = True

    return MockedMediaPlayer


@pytest.fixture()
def mocked_lt_parser():
    class MockedLTParser:
        def __init__(self, lyrics_path):
            self.lines_gotten = False
            self.time_actualized = False

        def get_next_n_lines(self, n):
            self.lines_gotten = True
            return []

        def actualize_time(self, time):
            self.time_actualized = True

    return MockedLTParser


@pytest.fixture()
def mocked_recorder():
    class MockedRecorder:
        def __init__(self, audio_path):
            self.is_recording = False
            self.saved = False

        def start_recording(self):
            self.is_recording = True
            self.saved = False

        def stop_recording(self):
            self.is_recording = False

        def save_overlapped(self):
            self.saved = True

    return MockedRecorder


@pytest.fixture()
def mocked_controller():
    class MockedController:
        def __init__(self, driver, drawer):
            self.activated = False
            self.song_audio_path = None
            self.song_lyrics_path = None

        def activate(self):
            self.activated = True

        def update_chosen_song(self, song_audio_path, song_lyrics_path):
            self.song_audio_path = song_audio_path
            self.song_lyrics_path = song_lyrics_path

    return MockedController
