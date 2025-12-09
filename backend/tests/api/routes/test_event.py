import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.event import EventCreate, EventUpdate

client = TestClient(app)


def test_create_event(test_event_data):
    response = client.post("/events/", json=test_event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_event_data["title"]
    assert data["description"] == test_event_data["description"]

def test_get_event(test_event_data):
    create_response = client.post("/events/", json=test_event_data)
    event_id = create_response.json()["id"]

    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["title"] == test_event_data["title"]

def test_list_all_events():
    response = client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_event(test_event_data):
    create_response = client.post("/events/", json=test_event_data)
    event_id = create_response.json()["id"]

    updated_data = {"title": "Updated Event", "description": "Updated description."}
    response = client.put(f"/events/{event_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]

def test_delete_event(test_event_data):
    create_response = client.post("/events/", json=test_event_data)
    event_id = create_response.json()["id"]

    response = client.delete(f"/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id

    get_response = client.get(f"/events/{event_id}")
    assert get_response.status_code == 404