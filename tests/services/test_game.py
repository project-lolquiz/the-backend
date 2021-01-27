from unittest import mock
import pytest

from models.game import GameType, GameMode
from services.game_service import get_all_types, get_all_modes


@mock.patch('services.game_service.db_all_types')
def test_get_all_types(mock_db_service):
    types_from_db = generate_mock_db_types()
    mock_db_service.return_value = types_from_db

    all_types = get_all_types()
    assert_response(all_types, types_from_db)


@mock.patch('services.game_service.db_all_modes')
def test_get_all_modes(mock_db_service):
    modes_from_db = generate_mock_db_modes()
    mock_db_service.return_value = modes_from_db

    all_modes = get_all_modes()
    assert_response(all_modes, modes_from_db)


def generate_mock_db_types():
    return [GameType('id' + str(index), 'Name_' + str(index), 'Description_' + str(index))
            for index in range(1, 4)]


def generate_mock_db_modes():
    return [GameMode('id' + str(index), 'Name_' + str(index), 'Description_' + str(index))
            for index in range(1, 4)]


def assert_response(response, list_db_value):
    assert response
    assert len(response) == len(list_db_value)

    for index in range(0, len(list_db_value)):
        content = response[index]
        from_db = list_db_value[index]
        assert 'id' in content
        assert 'name' in content
        assert 'description' in content
        assert content['id'] == from_db.id
        assert content['name'] == from_db.name
        assert content['description'] == from_db.description
