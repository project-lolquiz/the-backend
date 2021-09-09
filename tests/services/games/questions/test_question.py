import os
import pytest

os.environ['ENV'] = 'qa'

from services.games.questions.question_service import get_game_question, get_current_questions, select_random_question
from tests.services.games.test_game import create_game_room, request_start_game_body

from services.games.game_service import *

from tests.services.rooms.test_room import DEFAULT_TOTAL_ROUNDS


def test_get_game_question():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    game_question = get_game_question(room_id)
    assert_game_question(game_question)


def test_get_another_game_question():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    game_question_01 = get_game_question(room_id)
    assert_game_question(game_question_01)

    game_question_02 = get_game_question(room_id)
    assert_game_question(game_question_02)

    assert game_question_01['selected_user_id'] != game_question_02['selected_user_id']
    assert game_question_01['title'] != game_question_02['title']
    assert game_question_01['round']['current'] < game_question_02['round']['current']


def test_get_different_game_question_accordingly_to_total_rounds():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    selected_titles = []

    for _ in range(0, DEFAULT_TOTAL_ROUNDS):
        game_question = get_game_question(room_id)
        assert_game_question(game_question)

        current_title = game_question['title']
        assert current_title not in selected_titles

        selected_titles.append(current_title)


def assert_game_question(game_question):
    assert game_question is not None
    assert 'selected_user_id' in game_question
    assert 'title' in game_question
    assert 'options' in game_question
    assert len(game_question['options']) > 0
    assert 'round' in game_question
    assert 'current' in game_question['round']
    assert 'total' in game_question['round']
    assert 'draw' in game_question


def test_failure_game_question_with_room_not_found():
    room_id = '14UI'

    with pytest.raises(RoomNotFound, match='Room ID {} not found'.format(room_id)):
        get_game_question(room_id)


def test_get_all_random_questions():
    room_id = create_game_room()
    body = request_start_game_body()
    start_new_game(body, room_id)

    current_room = json.loads(get_by_key(room_id))
    questions_id = set()

    all_questions = get_current_questions(room_id, current_room)
    total_questions = len(all_questions)
    for _ in range(0, total_questions):
        question = select_random_question(room_id, current_room)
        assert question['id'] not in questions_id
        questions_id.add(question['id'])

    assert len(questions_id) == total_questions

    # After getting all questions randomly, should get one already selected
    question = select_random_question(room_id, current_room)
    assert question['id'] in questions_id
