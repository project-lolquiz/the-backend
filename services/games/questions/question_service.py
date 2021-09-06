import json
import random

from components.exception_component import RoomNotFound
from services.cms_service import get_questions_by_game_type_and_game_mode
from services.redis_service import set_content, get_by_key
from services.rooms.room_service import exists_room_by_id


def get_game_question(room_id):
    if not exists_room_by_id(room_id):
        raise RoomNotFound('Room ID {} not found'.format(room_id))

    current_room = json.loads(get_by_key(room_id))
    current_users = get_current_users(current_room)
    current_round = get_game_round(room_id, current_room)

    random_user = select_random_user(room_id, current_room)
    random_question = select_random_question(room_id, current_room)
    selected_question = set_question_options_with_users(random_question, current_users)

    response = {'selected_user_id': random_user,
                'title': selected_question['title'],
                'options': selected_question['options'],
                'round': current_round,
                'draw': False}  # TODO: adicionar logica para identificar empate (de acordo com as respostas armazenadas)

    current_room = json.loads(get_by_key(room_id))
    print("\ncurrent_room={}, round={}, selected_users={}, selected_questions={}".format(
        current_room,
        current_room['game']['round'],
        current_room['game']['selected_users'],
        current_room['game']['selected_questions']))
    return response


def get_current_questions(room_id, current_room):
    current_game = current_room['game']
    if 'questions' not in current_game:
        game_type_id = current_room['game_type']
        game_mode_id = current_room['game_mode']
        questions = get_questions_by_game_type_and_game_mode(game_type_id, game_mode_id)

        current_room['game']['questions'] = questions
        set_content(room_id, current_room)

    return current_room['game']['questions']


def get_current_users(current_room):
    host_user = current_room['host_user']
    users = current_room['game']['users']
    players = [player for player in users]
    players.append(host_user)
    return players


def get_game_round(room_id, current_room):
    current_game = current_room['game']
    if 'round' not in current_game:
        current_round = {'current': 0,
                         'total': current_room['total_rounds']}
        current_game['round'] = current_round

    current_game['round']['current'] = current_game['round']['current'] + 1
    current_room['game'] = current_game
    set_content(room_id, current_room)

    return current_game['round']


def get_selected_users(room_id, current_room):
    current_game = current_room['game']
    if 'selected_users' not in current_game:
        current_game['selected_users'] = []
        current_room['game'] = current_game
        set_content(room_id, current_room)

    return current_game['selected_users']


def get_selected_questions(room_id, current_room):
    current_game = current_room['game']
    if 'selected_questions' not in current_game:
        current_game['selected_questions'] = []
        current_room['game'] = current_game
        set_content(room_id, current_room)

    return current_game['selected_questions']


def update_selected_users(room_id, selected_user_uid, current_room):
    current_game = current_room['game']
    current_game['selected_users'].append(selected_user_uid)
    current_room['game'] = current_game
    set_content(room_id, current_room)


def update_selected_questions(room_id, selected_question, current_room):
    current_game = current_room['game']
    current_game['selected_questions'].append(selected_question['id'])
    current_room['game'] = current_game
    set_content(room_id, current_room)


def select_random_user(room_id, current_room):
    all_users = get_current_users(current_room)
    selected_users = get_selected_users(room_id, current_room)
    if all_users_already_played(all_users, selected_users):
        current_room['game']['selected_users'] = []
        selected_user = random.choice([selected_user['uid'] for selected_user in all_users])
    else:
        selected_user = random.choice([selected_user['uid']
                                       for selected_user in all_users
                                       if selected_user['uid'] not in selected_users])

    update_selected_users(room_id, selected_user, current_room)
    return selected_user


def all_users_already_played(all_players, selected_users):
    return len(all_players) == len(selected_users)


def select_random_question(room_id, current_room):
    all_questions = get_current_questions(room_id, current_room)
    selected_questions = get_selected_questions(room_id, current_room)
    if all_questions_already_played(all_questions, selected_questions):
        current_room['game']['selected_questions'] = []
        selected_question = random.choice([selected_question['id'] for selected_question in all_questions])
    else:
        selected_question = random.choice([question
                                           for question in all_questions
                                           if question['id'] not in selected_questions])

    update_selected_questions(room_id, selected_question, current_room)
    return selected_question


def all_questions_already_played(all_questions, selected_questions):
    return len(all_questions) == len(selected_questions)


def set_question_options_with_users(selected_question, current_users):
    if len(selected_question['options']) == 0:
        selected_question['options'] = [{'title': current_user['uid'],
                                         'description': current_user['nickname']}
                                        for current_user in current_users]
    return selected_question
