import json

from components.exception_component import QuestionsNotFound
from gateways.cms_gateway import get_questions
from services.redis_service import set_content, get_by_key

ALL_QUESTIONS_KEY = 'ALL_QUESTIONS'


def save_questions_on_redis():
    questions = get_questions()
    if questions is None:
        raise QuestionsNotFound("No questions were found")

    set_content(ALL_QUESTIONS_KEY, questions)


def get_all_questions():
    questions = get_by_key(ALL_QUESTIONS_KEY)
    if questions is None:
        save_questions_on_redis()
        questions = get_by_key(ALL_QUESTIONS_KEY)

    return json.loads(questions)


def get_questions_by_game_type_and_game_mode(game_type_id, game_mode_id):
    questions = get_all_questions()

    filtered_by_game_type = [question for question in questions if question['game_type']['id'] == game_type_id]
    filtered_by_game_mode = [question for question in filtered_by_game_type
                             if (same_game_mode_id(game_mode_id, question['game_modes']))]

    filtered_questions = [{'id': question['id'],
                           'title': question['title'],
                           'options': question['options']} for question in filtered_by_game_mode]

    return filtered_questions


def same_game_mode_id(game_mode_id, game_modes):
    ids = [game_mode['id'] for game_mode in game_modes]
    return game_mode_id in ids
