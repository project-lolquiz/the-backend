import os

from unittest import mock

import pytest

os.environ['ENV'] = 'qa'

from components.exception_component import QuestionsNotFound
from services.cms_service import ALL_QUESTIONS_KEY, save_questions_on_redis, get_all_questions, \
    get_questions_by_game_type_and_game_mode
from services.redis_service import get_by_key


def test_save_questions_on_redis():
    save_questions_on_redis()
    all_saved_questions = get_by_key(ALL_QUESTIONS_KEY)
    assert all_saved_questions is not None
    assert type(all_saved_questions) == str


@mock.patch('services.cms_service.get_questions')
def test_failure_save_questions_on_redis_with_questions_not_found(mock_get_questions):
    mock_get_questions.return_value = None

    with pytest.raises(QuestionsNotFound, match='No questions were found'):
        save_questions_on_redis()


def test_get_all_questions_when_already_in_redis():
    test_save_questions_on_redis()
    all_questions_as_json = get_all_questions()
    assert all_questions_as_json is not None
    assert type(all_questions_as_json) != str


@mock.patch('services.cms_service.get_by_key')
def test_get_all_questions_when_not_already_in_redis(mock_get_by_key):
    mock_get_by_key.side_effect = [None, '[{"id": 1, "title": "fake"}]']

    all_questions_as_json = get_all_questions()
    assert all_questions_as_json is not None
    assert type(all_questions_as_json) != str


@mock.patch('services.cms_service.get_questions')
@mock.patch('services.cms_service.get_by_key')
def test_failure_get_all_questions_with_questions_not_found(mock_get_by_key, mock_get_questions):
    mock_get_by_key.return_value = None
    mock_get_questions.return_value = None

    with pytest.raises(QuestionsNotFound, match='No questions were found'):
        get_all_questions()


def test_get_questions_by_game_type_and_game_mode():
    game_type_id = 2
    game_mode_id = 1

    questions = get_questions_by_game_type_and_game_mode(game_type_id, game_mode_id)
    assert questions is not None
    for question in questions:
        assert 'id' in question
        assert 'title' in question
        assert 'options' in question


@mock.patch('services.cms_service.get_questions')
@mock.patch('services.cms_service.get_by_key')
def test_failure_get_questions_by_game_type_and_game_mode_with_questions_not_found(mock_get_by_key, mock_get_questions):
    mock_get_by_key.return_value = None
    mock_get_questions.return_value = None

    with pytest.raises(QuestionsNotFound, match='No questions were found'):
        game_type_id = 2
        game_mode_id = 1
        get_questions_by_game_type_and_game_mode(game_type_id, game_mode_id)
