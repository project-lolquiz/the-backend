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
        raise QuestionsNotFound("No questions were found")

    return json.loads(questions)