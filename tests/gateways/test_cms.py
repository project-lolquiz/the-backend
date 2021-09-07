from gateways.cms_gateway import get_questions


def test_get_questions():
    response = get_questions()
    assert response is not None
    for question in response:
        assert 'id' in question
        assert 'game_type' in question
        assert 'game_modes' in question
        assert 'options' in question
