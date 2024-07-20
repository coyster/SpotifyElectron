from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.spotify_electron.genre.genre_schema import Genre
from tests.test_API.api_test_artist import create_artist, get_artist
from tests.test_API.api_test_song import (
    create_song,
    delete_song,
    get_song,
    get_songs_by_genre,
    increase_song_streams,
)
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


file_path = "tests/assets/song.mp3"
file_path_4s_song = "tests/assets/song_4_seconds.mp3"


def test_create_song_correct():
    """
    Feature: Song Management
    Scenario: Posting a song correctly
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3", genre "Pop", and\
         photo "https://photo"
    Then I should receive a 201 Created status code
    And the song should be created successfully
    """
    song_name = "song-name"
    genre = "Pop"
    photo = "https://photo"

    artist_name = "artist-name"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_create_song_as_user():
    """
    Feature: Song Management
    Scenario: Posting a song as a user who is also the artist
    Given a user "artist-name" with photo "https://photo" and password "password" exists
    When I create the user
    And attempt to create a song "song-name" with file_path "tests/assets/song.mp3"\
         , genre "Pop", and photo "https://photo"
    Then I should receive a 403 Forbidden status code
    """
    song_name = "song-name"
    genre = "Pop"
    photo = "https://photo"

    user_name = "artist-name"
    password = "password"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=user_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_403_FORBIDDEN

    res_delete_artist = delete_user(user_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_create_song_correct_check_valid_duration():
    """
    Feature: Song Management
    Scenario: Posting a song with valid duration
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song_4_seconds.mp3",\
          genre "Pop", and photo "https://photo"
    Then I should receive a 201 Created status code
    And the song should have a duration of 4 seconds
    And I should be able to retrieve the song
    """
    song_name = "song-name"
    genre = "Pop"
    photo = "https://photo"

    artist_name = "artist-name"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path_4s_song,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert str(res_get_song.json()["seconds_duration"]).split(".")[0] == "4"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_create_song_correct_check_invalid_duration():
    """
    Feature: Song Management
    Scenario: Posting a song with invalid duration
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    Then I should receive a 201 Created status code
    And the song should have a duration of 0 seconds
    And I should be able to retrieve the song
    """
    song_name = "song-name"
    genre = "Pop"
    photo = "https://photo"

    artist_name = "artist-name"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert "0" in str(res_get_song.json()["seconds_duration"])

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_song_correct():
    """
    Feature: Song Management
    Scenario: Retrieving a song correctly
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    And retrieve the song "song-name"
    Then I should receive a 200 OK status code
    And the retrieved song should have the correct details
    """
    song_name = "song-name"
    genre = "Pop"
    photo = "https://photo"

    artist_name = "artist-name"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert res_get_song.json()["name"] == song_name
    assert res_get_song.json()["artist"] == artist_name
    assert res_get_song.json()["genre"] == Genre(genre)
    assert res_get_song.json()["photo"] == photo

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_song_invalid_name():
    """
    Feature: Song Management
    Scenario: Retrieving a non-existent song
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And retrieve JWT headers for the artist
    And attempt to retrieve a song "song-name" that does not exist
    Then I should receive a 404 Not Found status code
    """
    song_name = "song-name"
    photo = "https://photo"

    artist_name = "artist-name"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_song_correct():
    """
    Feature: Song Management
    Scenario: Deleting a song correctly
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    And delete the song "song-name"
    Then I should receive a 202 Accepted status code
    And the song should be deleted successfully
    And the artist should have no uploaded songs
    """
    song_name = "song-name"
    artist_name = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_song_not_found():
    """
    Feature: Song Management
    Scenario: Deleting a non-existent song
    When I attempt to delete a song "song-name" that does not exist
    Then I should receive a 404 Not Found
    """
    song_name = "song-name"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_404_NOT_FOUND


def test_patch_number_plays_song_correct():
    """
    Feature: Song Management
    Scenario: Patching the number of plays for a song correctly
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    And patch the number of plays for the song "song-name"
    Then I should receive a 204 No Content status code
    And the song should have 1 play
    """
    song_name = "song-name"
    artist = "artist-name"
    genre = "Pop"
    photo = "https://photo"

    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_204_NO_CONTENT

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert res_get_song.json()["streams"] == 1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_number_of_plays_song_not_found():
    """
    Feature: Song Management
    Scenario: Patching the number of plays for a non-existent song
    When I attempt to patch the number of plays for a song "song-name" that does not exist
    Then I should receive a 404 Not Found status code
    """
    song_name = "song-name"
    artist = "artist-name"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    song_name = "song-name"

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_song_invalid_name():
    """
    Feature: Song Management
    Scenario: Patching the number of plays for a song with an invalid name
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And attempt to patch the number of plays for a song with an empty name
    Then I should receive a 404 Not Found status code
    """
    song_name = "song-name"
    artist = "artist-name"
    photo = "https://photo"

    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    song_name = ""

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_song_uploaded_songs_updated():
    """
    Feature: Song Management
    Scenario: Verifying uploaded songs are updated for an artist
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    And retrieve the artist "artist-name"
    Then the artist should have 1 uploaded song "song-name"

    """
    song_name = "song-name"
    artist = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_artist = get_artist(name=artist, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["uploaded_songs"]) == 1
    assert res_get_artist.json()["uploaded_songs"][0] == song_name

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_song_uploaded_songs_artist_not_found():
    """
    Feature: Song Management
    Scenario: Attempting to create a song for a non-existent artist
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I delete the artist
    And attempt to create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    Then I should receive a 404 Not Found status code
    """
    song_name = "song-name"
    artist = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_404_NOT_FOUND


def test_delete_song_uploaded_songs_updated():
    """
    Feature: Song Management
    Scenario: Deleting a song updates uploaded songs for an artist
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Pop", and photo "https://photo"
    And delete the song "song-name"
    Then the artist should have 0 uploaded songs
    """
    song_name = "song-name"
    artist = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_get_artist = get_artist(name=artist, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["uploaded_songs"]) == 0

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_song_by_genre():
    """
    Feature: Song Management
    Scenario: Retrieving songs by genre
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And create a song "song-name" with file_path "tests/assets/song.mp3",\
          genre "Rock", and photo "https://photo"
    And retrieve songs by genre "Rock"
    Then I should receive a 200 OK status code
    And I should receive a list of songs with length 1
    """
    song_name = "song-name"
    artist = "artist-name"
    genre = "Rock"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song_by_genre = get_songs_by_genre(genre=genre, headers=jwt_headers)
    assert res_get_song_by_genre.status_code == HTTP_200_OK
    assert len(res_get_song_by_genre.json()) == 1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_song_by_genre_bad_genre():
    """
    Feature: Song Management
    Scenario: Attempting to retrieve songs with a non-existent genre
    Given an artist "artist-name" with photo "https://photo" and password "password" exists
    When I create the artist
    And attempt to retrieve songs by genre "NonExistingGenre"
    Then I should receive a 422 Unprocessable Entity status code
    And I should be able to delete the artist
    """
    genre = "NonExistingGenre"

    artist = "artist-name"
    photo = "https://photo"
    password = "password"

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_get_song_by_genre = get_songs_by_genre(genre=genre, headers=jwt_headers)
    assert res_get_song_by_genre.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED
