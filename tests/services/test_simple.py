from unittest import mock

from models.simple import Simple
from services.simple_service import add, get_by_id, get_all


@mock.patch('services.simple_service.Simple.add_new')
def test_add(mock_db_service):
    content = {'value': 'a content'}
    mock_db_service.return_value = None
    add(content)


@mock.patch('services.simple_service.Simple')
def test_get_by_id(mock_db_service):
    from_db = Simple('new content')
    from_db.id = 1
    mock_db_service.query.filter_by.return_value.first_or_404.return_value = from_db

    response = get_by_id(from_db.id)
    assert response
    assert 'id' in response
    assert response['id'] == from_db.id
    assert 'value' in response
    assert response['value'] == from_db.name


@mock.patch('services.simple_service.Simple')
def test_get_all(mock_db_service):
    from_db = mock_db_content()
    mock_db_service.query.all.return_value = from_db

    response = get_all()
    assert response
    assert len(response) == len(from_db)

    for index in range(0, len(from_db)):
        simple_response = response[index]
        simple_from_db = from_db[index]

        assert 'id' in simple_response
        assert simple_response['id'] == simple_from_db.id
        assert 'value' in simple_response
        assert simple_response['value'] == simple_from_db.name


def mock_db_content():
    from_db_1 = Simple('first content')
    from_db_1.id = 1

    from_db_2 = Simple('second content')
    from_db_2.id = 2

    return [from_db_1, from_db_2]