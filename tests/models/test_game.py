import os
os.environ['ENV'] = 'qa'

from unittest import mock

from models.game import GameMode, get_all_modes, GameType, get_all_types


@mock.patch('models.game.GameType')
def test_get_all_types(mock_game_type):
    first_type = GameType(1, 'name 1', 'description 1')
    mock_game_type.query.all.return_value = [first_type]

    all_types = get_all_types()
    assert len(all_types) == 1
    assert all_types[0].id == first_type.id
    assert all_types[0].name == first_type.name
    assert all_types[0].description == first_type.description


@mock.patch('models.game.GameMode')
def test_get_all_modes(mock_game_modes):
    first_mode = GameMode(1, 'name 1', 'description 1')
    mock_game_modes.query.all.return_value = [first_mode]

    all_modes = get_all_modes()
    assert len(all_modes) == 1
    assert all_modes[0].id == first_mode.id
    assert all_modes[0].name == first_mode.name
    assert all_modes[0].description == first_mode.description
