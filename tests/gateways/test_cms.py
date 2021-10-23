from gateways.cms_gateway import get_questions, valid_question


def test_get_questions():
    response = get_questions()
    assert response is not None
    valid_questions = [valid_question(question) for question in response]
    assert False not in valid_questions
