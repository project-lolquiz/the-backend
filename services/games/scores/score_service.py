import json

from components.exception_component import RoomNotFound
from services.games.players.player_service import get_current_players
from services.redis_service import set_content, get_by_key
from services.rooms.room_service import exists_room_by_id

DEFAULT_SCORE_FACTOR = 10


def get_game_total_score(current_room):
    current_users = get_current_players(current_room)
    total_users = len(current_users)
    return total_users * DEFAULT_SCORE_FACTOR


def get_score_by_users(room_id, current_room):
    current_game = current_room['game']
    if 'score_by_user' not in current_game:
        current_game['score_by_user'] = []
        current_room['game'] = current_game
        set_content(room_id, current_room)

    return current_game['score_by_user']


def update_users_score(room_id, current_room, users_score):
    current_game = current_room['game']
    current_game['score_by_user'] = users_score
    current_room['game'] = current_game
    set_content(room_id, current_room)


def is_draw_game(current_scores):
    highest_score = get_highest_score(current_scores)
    total_times_highest_score = [times_highest_score for times_highest_score in current_scores
                                 if times_highest_score['total_score'] == highest_score]
    return len(total_times_highest_score) > 1


def get_highest_score(current_scores):
    highest_score = 0
    for user_score in current_scores:
        if user_score['total_score'] > highest_score:
            highest_score = user_score['total_score']
    return highest_score


def get_result_score(room_id):
    if not exists_room_by_id(room_id):
        raise RoomNotFound('Room ID {} not found'.format(room_id))

    current_room = json.loads(get_by_key(room_id))
    score_by_user = current_room['game']['score_by_user']
    winner = get_user_with_highest_score(score_by_user)

    return {'users': score_by_user,
            'winner': winner}


def get_user_with_highest_score(score_by_user):
    highest_score = get_highest_score(score_by_user)
    users_with_highest_score = [user for user in score_by_user if user['total_score'] == highest_score]
    if len(users_with_highest_score) == 1:
        return users_with_highest_score[0]
    return None
