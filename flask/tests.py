'''
To run these tests:
$ pip install pytest
$ pytest tests.py
'''
import pytest
import re
from api import app
from flask import Response

MAX_COUNT = 100
MAX_LENGTH = 25

@pytest.fixture
def application_context():
    app.config.update({
        "TESTING": True
    })
    created_ids = set()
    yield app, created_ids
    for id in created_ids:
        response = app.test_client().delete(f"/synth/{id}")
        assert response.status_code in (204, 404)

@pytest.fixture
def client(application_context):
    application, _ = application_context
    return application.test_client()

@pytest.fixture
def created_ids(application_context):
    _, created_ids = application_context
    return created_ids


def test_create_and_delete(client):
    response = client.post("/synth", json={
        "frequency": 440,
        "seconds": 1
    })
    assert response.status_code == 201
    
    id = response.get_id()
    assert id == 1

    delete_response = client.delete(f"/synth/{id}")
    assert delete_response.status_code == 204

    get_response_after_deletion = client.get(f"/static/{id}.wav")
    assert get_response_after_deletion.status_code == 404

def test_delete_all_successfully(client, created_ids):
    response_urls = list()
    for _ in range(3):
        response = client.post("/synth", json={
            "frequency": 150,
            "seconds": 1
        })
        id = response.get_id()
        response_urls.append(f"/static/{id}.wav")
        created_ids.add(id)

    delete_response = client.delete("/delete")
    assert delete_response.status_code == 204
    
    for url in response_urls:
        response = client.get(url)
        assert response.status_code == 404

def test_error_after_creating_too_many_files(client, created_ids):
    assert client.delete("/delete").status_code == 204

    for i in range(MAX_COUNT + 2):
        response = client.post("/synth", json={
            "frequency": 100,
            "seconds": 0
        })
        if (i == MAX_COUNT + 1):
            assert client.delete("/delete").status_code == 204
            assert response.status_code == 503

def test_not_found_if_delete_id_does_not_exist(client):
    response = client.delete(f"/synth/1000")
    assert response.status_code == 404


def test_information(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_successful_after_post(client, created_ids):
    response = client.post("/synth", json={
        "frequency": 110,
        "seconds": 0.1,
    })
    assert response.status_code == 201

    id = response.get_id()

    get_response = client.get(f"/static/{id}.wav")
    assert get_response.status_code == 200
    created_ids.add(id)


def test_can_create_all_wave_types(client, created_ids):
    for waveform in ('sine', 'triangular', 'sawtooth', 'square'):
        response = client.post("/synth", json={
            "frequency": 440,
            "seconds": 1,
            "waveform": waveform
        })
        assert response.status_code == 201
        created_ids.add(response.get_id())


def test_can_create_envelope(client, created_ids):
    envelope = {"attack": 0.1, "decay": 0.2, "release": 0.1}
    response = client.post("/synth", json={
        "frequency": 440,
        "seconds": 1,
        "envelope": envelope
    })
    assert response.status_code == 201
    created_ids.add(response.get_id())


def test_not_all_envelope_parameters_are_necessary(client, created_ids):
    envelope = {"decay": 0.4, "release": 0.1}
    response = client.post("/synth", json={
        "frequency": 440,
        "seconds": 1,
        "envelope": envelope
    })
    assert response.status_code == 201
    created_ids.add(response.get_id())
    

def test_using_all_parameters_work(client, created_ids):
    envelope = {"attack": 0.1, "decay":0.2, "release": 0.2}
    response = client.post("/synth", json={
        "frequency": 440,
        "seconds": 1,
        "amplitude": 0.05,
        "envelope": envelope,
        "waveform": "triangular",
    })
    assert response.status_code == 201
    created_ids.add(response.get_id())

def test_cannot_create_overly_long_files(client, created_ids):
    response = client.post("/synth", json={
        "frequency": 880,
        "seconds": MAX_LENGTH + 1
    })
    assert response.status_code == 400


def get_id(self):
    assert 'Location' in self.headers.keys()
    location = self.headers['Location']
    id_expression = re.compile(r'/[1-9]*\.')
    id = int(id_expression.search(location).group()[1:-1])
    '''
    url_expression = re.compile('.*/static')
    url = url_expression.search(location).group()[:-7]
    delete_url = f"{url}/synth/{id}"
    '''
    return id
Response.get_id = get_id