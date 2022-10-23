def test_tick(main_menu_controller):
    main_menu_controller.tick()

    assert main_menu_controller.drawer.drawn


def test_refresh_songs(main_menu_controller):
    main_menu_controller.refresh_songs()

    assert main_menu_controller.drawer.song_selector_updated


def test_activate(main_menu_controller):
    assert main_menu_controller.drawer.activated


def test_start_playing(main_menu_controller):
    main_menu_controller.start_playing()

    assert main_menu_controller.driver.song_audio_path == 'lolkek.mp3'
    assert main_menu_controller.driver.song_lyrics_path == 'lolkek.lt'
