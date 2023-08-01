from fastapi.testclient import TestClient
from fastapi import UploadFile
import io
import json
import pytest

from main import app as app


client = TestClient(app)


def test_post_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"

    url = f"/canciones/?nombre={song_name}&artista=artista&genero=Pop&foto=foto"

    with open('__tests__/song.mp3', 'rb') as file:
        response = client.post(url, files={'file': file})
        assert response.status_code == 201

    response = client.delete(f"/canciones/{song_name}")
    assert response.status_code == 202


def test_get_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"

    url = f"/canciones/?nombre={song_name}&artista=artista&genero=Pop&foto=foto"

    with open('__tests__/song.mp3', 'rb') as file:
        response = client.post(url, files={'file': file})
        assert response.status_code == 201

    response = client.get(f"/canciones/{song_name}")
    assert response.status_code == 200

    response = client.delete(f"/canciones/{song_name}")
    assert response.status_code == 202


def test_get_cancion_invalid_name():

    song_name = "8232392323623823723989"

    response = client.get(f"/canciones/{song_name}")
    assert response.status_code == 404


def test_post_cancion_invalid_param_():

    song_name = "8232392323623823723989"

    url = f"/canciones/?nombre={song_name}&artista=&genero=Pop&foto=foto"

    with open('__tests__/song.mp3', 'rb') as file:
        response = client.post(url, files={'file': file})
        assert response.status_code == 400


def test_delete_cancion_correct():

    song_name = "8232392323623823723989"

    url = f"/canciones/?nombre={song_name}&artista=artista&genero=Pop&foto=foto"

    with open('__tests__/song.mp3', 'rb') as file:
        response = client.post(url, files={'file': file})
        assert response.status_code == 201

    response = client.delete(f"/canciones/{song_name}")
    assert response.status_code == 202


def test_delete_cancion_not_found():

    song_name = "8232392323623823723989"

    response = client.delete(f"/canciones/{song_name}")
    assert response.status_code == 404


def test_get_canciones_correct():
    response = client.get(f"/canciones/")
    assert response.status_code == 200


@pytest.fixture()
def clear_test_data_db():
    song_name = "8232392323623823723989"
    response = client.delete(f"/canciones/{song_name}")

    yield
    song_name = "8232392323623823723989"
    response = client.delete(f"/canciones/{song_name}")