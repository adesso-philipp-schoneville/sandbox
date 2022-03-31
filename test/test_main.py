from src import main
import pytest


@pytest.fixture
def client():
    """
    Function that prepares Flask for testing.
    :return: Flask client
    """
    app = main.app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_process(client):
    """
    Function that tests the /process route.
    :param client:
    :return: None
    """

    request = {"message": "Hi, this is a test message..."}
    response = client.post("/process", json=request)

    assert response.status_code == 200
    assert response.json == {"lengthOfMessage": 29}
