'''
To run these tests:
$ pip install pytest
$ pytest tests.py
'''
import pytest
import re
from api import app
from flask import Response

@pytest.fixture
def application_context():
    app.config.update({
        "TESTING": True
    })
    created_ids = set()
    yield app, created_ids
    for id in created_ids:
        response = app.test_client().delete(f"/synth/{id}")
        assert response.status_code == 204

@pytest.fixture
def client(application_context):
    application, _ = application_context
    return application.test_client()

@pytest.fixture
def created_ids(application_context):
    _, created_ids = application_context
    return created_ids


def test_create_and_delete(client, created_ids):
    response = client.post("/synth", json={
        "frequency": 440,
        "seconds": 1
    })
    assert response.status_code == 201
    
    id = response.get_id()
    assert id == 1

    delete_response = client.delete(f"/synth/{id}")
    assert delete_response.status_code == 204


def test_not_found_if_delete_id_does_not_exist(client):
    response = client.delete(f"/synth/1")
    assert response.status_code == 404


def test_information(client):
    response = client.get("/")
    assert response.status_code == 200


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