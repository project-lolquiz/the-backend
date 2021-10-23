import requests
import json

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOLQUIZ_CMS_URL = 'https://lolquiz-cms.herokuapp.com/questions?_sort=id&_limit={}&_start={}'
HTTP_STATUS_ERROR_CODES = [408, 502, 503, 504]
TOTAL_QUESTIONS = 100
INIT_OFFSET = 0


def get_questions(url=LOLQUIZ_CMS_URL):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=HTTP_STATUS_ERROR_CODES)
    s.mount('https://', HTTPAdapter(max_retries=retries))

    offset = INIT_OFFSET
    all_questions = []
    while True:
        url = LOLQUIZ_CMS_URL.format(TOTAL_QUESTIONS, offset)
        response = s.get(url)
        if not has_content(response):
            break
        all_questions.append(json.loads(response.content))
        offset += TOTAL_QUESTIONS

    return [set_question(question)
            for outer_questions in all_questions
            for question in outer_questions if valid_question(question)]


def has_content(response):
    return len(json.loads(response.content)) > 0


def valid_question(question):
    return 'id' in question \
           and 'title' in question \
           and 'game_type' in question and question['game_type'] is not None \
           and 'game_modes' in question and len(question['game_modes']) > 0 \
           and 'options' in question


def set_question(question):
    return {'id': question['id'],
            'title': question['title'],
            'game_type': question['game_type'],
            'options': question['options'],
            'game_modes': question['game_modes']}
