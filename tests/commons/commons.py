import json

APPLICATION_JSON = 'application/json'


def assert_room_not_found(response, room_id):
    assert response
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 404

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' in response_content
    assert response_content['error'] == 'Room ID {} not found'.format(room_id)


def assert_failure_missing_property(response, missing_property):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 400

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' not in response_content
    assert response_content['error'] == '\'{}\' is a required property'.format(missing_property)


def assert_generic_error(response, error_message):
    assert response.data
    assert response.content_type == APPLICATION_JSON
    assert response.status_code == 500

    response_content = json.loads(response.get_data(as_text=True))
    assert 'error' in response_content
    assert 'timestamp' in response_content
    assert response_content['error'] == error_message
