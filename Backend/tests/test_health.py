from fastapi.testclient import TestClient
from pytest import fixture
from starlette.status import HTTP_200_OK

from app.__main__ import app

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_health_check():
    """
    Feature: Health endpoint
    Scenario: Checking the health of the service
        Given the application is running
        When I send a GET request to the /health/ endpoint
        Then I should receive a 200 OK status code
        And the response text should be "OK"
    """
    response = client.get("/health/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "OK"
