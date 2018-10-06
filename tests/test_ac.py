import pytest

import ac


@pytest.fixture
def client():
    ac.app.config['TESTING'] = True
    client = ac.app.test_client()

    yield client
