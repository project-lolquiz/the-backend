import json

from components.exception_component import RoomNotFound
from services.games.players.player_service import get_current_players
from services.games.questions.question_service import get_game_round
from services.games.scores.score_service import get_game_total_score, get_score_by_users, update_users_score, \
    is_draw_game
from services.redis_service import get_by_key
from services.rooms.room_service import exists_room_by_id


def set_answer(room_id, content):
    if not exists_room_by_id(room_id):
        raise RoomNotFound('Room ID {} not found'.format(room_id))

    answer_data = json.loads(json.dumps(content))
    selected_user_id = answer_data['selected_user_id']
    user_answers = answer_data['users']

    users_with_right_answer = [user_answer['uid'] for user_answer in user_answers
                               if not is_selected_user(user_answer, selected_user_id)
                               and is_right_answer(user_answer, selected_user_id)]
    users_with_wrong_answer = [user_answer['uid'] for user_answer in user_answers
                               if not is_selected_user(user_answer, selected_user_id)
                               and not is_right_answer(user_answer, selected_user_id)]

    current_room = json.loads(get_by_key(room_id))
    total_score = get_game_total_score(current_room)

    current_scores = []
    current_game_status = []

    current_users = get_current_players(current_room)
    score_by_users = get_score_by_users(room_id, current_room)

    if len(users_with_right_answer) > 0:
        score_for_users_with_right_answer = total_score / len(users_with_right_answer)
        current_scores = update_user_score(users_with_right_answer,
                                           score_for_users_with_right_answer,
                                           current_scores,
                                           current_users,
                                           score_by_users)
        selected_user_score = update_selected_user_score(selected_user_id,
                                                         score_by_users,
                                                         current_users,
                                                         5 * len(users_with_right_answer))
        current_scores.append(selected_user_score)
        current_game_status = set_current_game_status_by_user(users_with_right_answer, True, current_game_status)
    else:
        # For current selected user
        updated_user_score = update_selected_user_score(selected_user_id,
                                                        score_by_users,
                                                        current_users,
                                                        total_score)
        current_scores.append(updated_user_score)

    if len(users_with_wrong_answer) > 0:
        current_scores = update_user_score(users_with_wrong_answer,
                                           0,
                                           current_scores,
                                           current_users,
                                           score_by_users)
        current_game_status = set_current_game_status_by_user(users_with_wrong_answer, False, current_game_status)

    update_users_score(room_id, current_room, current_scores)
    current_game_status = set_current_game_status_for_selected_user(selected_user_id, current_game_status)

    draw_game = False
    end_game = is_end_game(room_id, current_room)
    if end_game:
        draw_game = is_draw_game(current_scores)

    return {'users': current_game_status,
            'draw': draw_game,
            'end_game': end_game}


def is_selected_user(user_answer, selected_user_uid):
    return user_answer['uid'] == selected_user_uid


def is_right_answer(user_answer, selected_user_uid):
    return user_answer['chosen_answer'] == selected_user_uid


def update_user_score(users_answer, score, current_scores, current_users, score_by_users):
    for user_answer in users_answer:
        user_score = [user for user in score_by_users if user['uid'] == user_answer]
        current_user = [user for user in current_users if user['uid'] == user_answer]
        updated_user_score = set_user_score(user_score, current_user, score)
        current_scores.append(updated_user_score)

    return current_scores


def update_selected_user_score(selected_user_id, score_by_users, current_users, score):
    user_score = [user for user in score_by_users if user['uid'] == selected_user_id]
    current_selected_user = [user for user in current_users if user['uid'] == selected_user_id]
    return set_user_score(user_score, current_selected_user, score)


def set_user_score(user_score, current_user, score):
    if len(user_score) == 0:
        current_user = current_user[0]
        user_score = {'uid': current_user['uid'],
                      'nickname': current_user['nickname'],
                      'total_score': score}
    else:
        user_score = user_score[0]
        user_score['total_score'] = user_score['total_score'] + score

    return user_score


def set_current_game_status_by_user(users_answer, correct_answer, current_game_status):
    for user_answer in users_answer:
        current_game_status.append({'uid': user_answer,
                                    'correct_answer': correct_answer,
                                    'selected_user': False})
    return current_game_status


def set_current_game_status_for_selected_user(selected_user_id, current_game_status):
    current_game_status.append({'uid': selected_user_id,
                                'correct_answer': False,
                                'selected_user': True})
    return current_game_status


def is_end_game(room_id, current_room):
    current_round = get_game_round(room_id, current_room)
    return current_round['current'] == current_round['total']