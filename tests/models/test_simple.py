from unittest import mock

from models.simple import Simple


@mock.patch('models.simple.db.session')
@mock.patch('models.simple.Simple')
def test_add_new(mock_db, mock_connection):
    new_simple = Simple('a simple object')

    from_db = new_simple
    from_db.id = 1

    mock_db.add_new.return_value = from_db
    mock_connection.commit.return_value = None
    mock_connection.flush.return_value = None

    response = new_simple.add_new()
    assert response
    assert response.id == from_db.id
    assert response.name == new_simple.name
