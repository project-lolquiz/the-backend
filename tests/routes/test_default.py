import pytest

import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            yield client


def test_default_route(client):
    response = client.get("/")
    assert_default_response_routes(response)


def test_health_route(client):
    response = client.get("/health")
    assert_default_response_routes(response)


def test_ping_route(client):
    response = client.get("/ping")
    assert_default_response_routes(response)


def test_not_found_route(client):
    response = client.get("/pingy")
    assert_default_response_routes(response, b'<strong>It seems this is not correct :-(</strong>', 404)


def assert_default_response_routes(response, message=b'pong', status_code=200, content_type='text/html; charset=utf-8'):
    assert response.data
    assert response.data == message
    assert response.status_code == status_code
    assert response.content_type == content_type
