import pytest
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate



def test_register_user(client_with_admin):
    user_data = {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "securepassword",
        "role": "user",
    }

    response = client_with_admin.post("/users/register", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["name"] == user_data["name"]
    assert created_user["role"] == user_data["role"]


def test_register_user_duplicate_email(client_with_admin):
    user_data = {
        "email": "duplicateuser@example.com",
        "name": "Duplicate User",
        "password": "securepassword",
        "role": "user",
    }

    # Register the user once
    client_with_admin.post("/users/register", json=user_data)

    # Attempt to register the same user again
    response = client_with_admin.post("/users/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "A user with this email already exists."


def test_get_user_by_id(client_with_admin, test_user):
    response = client_with_admin.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    fetched_user = response.json()
    assert fetched_user["id"] == test_user["id"]
    assert fetched_user["email"] == test_user["email"]


def test_get_user_not_found(client_with_admin):
    response = client_with_admin.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_list_users(client_with_admin, test_user):
    response = client_with_admin.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert any(user["id"] == test_user["id"] for user in users)

