from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)

from tests.test_API.api_test_playlist import create_playlist, delete_playlist
from tests.test_API.api_test_search import get_search_by_name
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_search_by_name_correct():
    """
    Feature: Search Functionality
    Scenario: Search by items name
    Given a user "user-name" with photo "https://photo" and password "password" exists
    When I create the user
    And create a playlist "playlist-name" with description "password" and photo "https://photo"
    And search for the playlist by name "playlist-name"
    Then I should receive a 200 OK status code
    And the search result should contain the playlist "playlist-name"
    """
    # TODO, crear los demas items y comprobarlos
    name = "user-name"
    photo = "https://photo"
    description = "password"
    password = "password"
    playlist_name = "playlist-name"

    res_create_user = create_user(name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name,
        description=description,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_search_by_name = get_search_by_name("playlist-name", jwt_headers)
    assert res_search_by_name.status_code == HTTP_200_OK
    assert res_search_by_name.json()["playlists"][0]["name"] == playlist_name

    res_delete_playlist = delete_playlist(name=playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_get_search_by_name_invalid_name():
    name = "user-name"
    photo = "https://photo"
    password = "password"

    res_create_user = create_user(name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_search_by_name = get_search_by_name("", jwt_headers)
    assert res_search_by_name.status_code == HTTP_400_BAD_REQUEST

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED
