import os
import pytest
from app.application import create_app


os.environ.setdefault('FLASK_CONFIG_MODULE', 'app.config')


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        # initialize before testing
        with app.app_context():
            pass
        yield client
    # clear after testing
    pass


def test_api(client):
    rv = client.get('/')
    assert rv.status_code == 200
