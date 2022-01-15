import pytest


from gui.dimension_calculations import calculate_screen_data


def test_calculate_screen_data():
    origin_x, origin_y, ratio = calculate_screen_data(800, 600, 800, 600)
    assert origin_x == 0
    assert origin_y == 0
    assert ratio == 1.0

    origin_x, origin_y, ratio = calculate_screen_data(800, 600, 1600, 600)
    assert origin_x == 400
    assert origin_y == 0
    assert ratio == 1.0

    origin_x, origin_y, ratio = calculate_screen_data(800, 600, 800, 1200)
    assert origin_x == 0
    assert origin_y == 300
    assert ratio == 1.0

    origin_x, origin_y, ratio = calculate_screen_data(800, 600, 1600, 1200)
    assert origin_x == 0
    assert origin_y == 0
    assert ratio == 2.0

