import pytest
from fastapi.testclient import TestClient


def test_create_event(client_with_admin):
    event_data = {
        "title": "New Event",
        "description": "This is a new event.",
        "location": "New York",
        "event_date": "2023-12-25T18:00:00Z",
        "total_tickets": 100,
        "available_tickets": 100,
    }

    response = client_with_admin.post("/events/?ticket_price=50.0", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert data["location"] == event_data["location"]
    assert data["event_date"].startswith("2023-12-25T18:00:00")
    assert data["total_tickets"] == event_data["total_tickets"]
    assert data["available_tickets"] == event_data["available_tickets"]


def test_get_event(client_with_admin):
    event_data = {
        "title": "Sample Event",
        "description": "Sample description.",
        "location": "Los Angeles",
        "event_date": "2023-12-31T20:00:00Z",
        "total_tickets": 50,
        "available_tickets": 50,
    }
    create_response = client_with_admin.post("/events/?ticket_price=30.0", json=event_data)
    assert create_response.status_code == 200
    created_event = create_response.json()

    response = client_with_admin.get(f"/events/{created_event['id']}")
    assert response.status_code == 200
    fetched_event = response.json()
    assert fetched_event["id"] == created_event["id"]
    assert fetched_event["title"] == created_event["title"]


def test_update_event(client_with_admin):
    event_data = {
        "title": "Event to Update",
        "description": "Description before update.",
        "location": "Chicago",
        "event_date": "2023-11-15T15:00:00Z",
        "total_tickets": 30,
        "available_tickets": 30,
    }
    create_response = client_with_admin.post("/events/?ticket_price=40.0", json=event_data)
    assert create_response.status_code == 200
    created_event = create_response.json()

    update_data = {"title": "Updated Event Title"}
    update_response = client_with_admin.put(
        f"/events/{created_event['id']}", json=update_data
    )
    assert update_response.status_code == 200
    updated_event = update_response.json()
    assert updated_event["title"] == update_data["title"]
    assert updated_event["id"] == created_event["id"]


def test_delete_event(client_with_admin):
    event_data = {
        "title": "Event to Delete",
        "description": "This event will be deleted.",
        "location": "San Francisco",
        "event_date": "2023-10-10T10:00:00Z",
        "total_tickets": 20,
        "available_tickets": 20,
    }
    create_response = client_with_admin.post("/events/?ticket_price=20.0", json=event_data)
    assert create_response.status_code == 200
    created_event = create_response.json()

    delete_response = client_with_admin.delete(f"/events/{created_event['id']}")
    assert delete_response.status_code == 200
    deleted_event = delete_response.json()
    assert deleted_event["id"] == created_event["id"]

    get_response = client_with_admin.get(f"/events/{created_event['id']}")
    assert get_response.status_code == 404


def test_get_nonexistent_event(client_with_admin):
    response = client_with_admin.get("/events/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."


def test_delete_nonexistent_event(client_with_admin):
    response = client_with_admin.delete("/events/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."