def test_unauthorized_access(client_with_user, db):
    payload = {
        "email": "unauthorized@example.com",
        "password": "password123",
        "full_name": "Unauthorized User",
    }

    response = client_with_user.post("/users/register", json=payload)
    assert response.status_code == 403
    assert response.json()["detail"] == "The user doesn't have enough privileges to access this resource"
