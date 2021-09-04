import requests
import json

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOLQUIZ_CMS_URL = 'https://lolquiz-cms.herokuapp.com/questions?_sort=id'
HTTP_STATUS_ERROR_CODES = [408, 502, 503, 504]


def get_questions(url=LOLQUIZ_CMS_URL):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=HTTP_STATUS_ERROR_CODES)
    s.mount('https://', HTTPAdapter(max_retries=retries))

    response = s.get(url)
    response_as_json = json.loads(response.content)

    return response_as_json
