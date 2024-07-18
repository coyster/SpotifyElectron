from datetime import datetime

import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

import app.auth.auth_service as auth_service
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.user.user_service as user_service
from app.auth.auth_schema import VerifyPasswordException
from app.spotify_electron.utils.date.date_utils import date_format
from tests.test_API.api_test_user import create_user, delete_user, get_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_user_correct():
    """
    Feature: User Management
    Scenario: Getting a user correctly
    Given a user with name "user-name" and photo "https://photo" and password "password" exists
    When I create the user
    Then I send a GET request to retrieve the user
    Then I should receive a 200 OK status code
    And the response JSON should contain the correct name and photo
    And the registration date from the response should match the creation time
    """
    name = "user-name"
    photo = "https://photo"
    password = "password"

    creation_date = datetime.strptime(
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), date_format
    )

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_get_user = get_user(name=name, headers=jwt_headers)
    assert res_get_user.status_code == HTTP_200_OK
    assert res_get_user.json()["name"] == name
    assert res_get_user.json()["photo"] == photo

    response_creation_date = res_get_user.json()["register_date"]
    response_creation_datetime = datetime.strptime(response_creation_date, date_format)

    assert creation_date.hour == response_creation_datetime.hour

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_get_user_not_found():
    """
    Feature: User Management
    Scenario: Getting a user that does not exist
    Given a user with name "user-name" does not exist
    When I attempt to delete the user
    Then I should receive a 404 Not Found status code
    """
    name = "user-name"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_404_NOT_FOUND


def test_create_user_correct():
    """
    Feature: User Management
    Scenario: Creating a user correctly
    Given a user with name "user-name", photo "https://photo", and password "password"
    When I create the user
    Then I should receive a 201 Created status code
    And the user should be created successfully
    """
    name = "user-name"
    photo = "https://photo"
    password = "password"

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_user_correct():
    """
    Feature: User Management
    Scenario: Deleting a user correctly
    Given a user with name "user-name", photo "https://photo", and password "password" exists
    When I delete the user
    Then I should receive a 202 Accepted status code
    """
    name = "user-name"
    photo = "https://photo"
    password = "password"

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_user_not_found():
    """
    Feature: User Management
    Scenario: Deleting a non-existent user
    Given a user with name "user-name" does not exist
    When I attempt to delete the user
    Then I should receive a 404 Not Found status code
    """
    name = "user-name"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_404_NOT_FOUND


def test_delete_user_invalid_name():
    """
    Feature: User Management
    Scenario: Deleting a user with an invalid name
    Given an invalid user name ""
    When I attempt to delete the user
    Then I should receive a 405 Method Not Allowed status code
    """
    name = ""

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_check_encrypted_password_correct():
    """
    Feature: User Password Management
    Scenario: Checking the encryption of the correct password
    Given a user with name "user-name", photo "https://photo", and password "password" exists
    When I create the user
    And retrieve the encrypted password for the user
    And verify the original password against the encrypted password
    Then the verification should be successful
    """
    name = "user-name"
    photo = "https://photo"
    password = "password"
    user_service.create_user(name, photo, password)
    generated_password = base_user_service.get_user_password(name)

    auth_service.verify_password(password, generated_password)
    base_user_service.delete_user(name)


def test_check_encrypted_password_different():
    """
    Feature: User Password Management
    Scenario: Checking the encryption with a different password
    Given a user with name "user-name", photo "https://photo", and password "password" exists
    When I create the user
    And retrieve the encrypted password for the user
    And verify a different password "password2" against the encrypted password
    Then the verification should fail
    """
    name = "user-name"
    photo = "https://photo"
    password = "password"
    user_service.create_user(name, photo, password)
    password = "password2"
    generated_password = base_user_service.get_user_password(name)
    with pytest.raises(VerifyPasswordException):
        auth_service.verify_password(password, generated_password)

    base_user_service.delete_user(name)
