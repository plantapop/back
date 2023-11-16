import random
import string
from uuid import uuid4

import pytest


@pytest.fixture
def body(app_version):
    return {
        "app_version": app_version,
        "name": "test",
        "surnames": ["Super", "Test"],
        "generate_token": True,
        "password": "".join([random.choice(string.ascii_letters) for _ in range(15)]),
        "email": "random_emai@gmail.com",
        "prefered_language": ["es"],
        "timezone": "Europe/Madrid",
    }


@pytest.mark.acceptance
def test_create_account(client, body):
    # When
    response = client.post("/user/", json=body)
    token = response.json()["token"]
    registration = response.json()["registration"]

    # Then
    assert response.status_code == 201
    assert registration["name"] == body["name"]
    assert registration["surnames"] == body["surnames"]
    assert registration["email"] == body["email"]
    assert registration["prefered_language"] == body["prefered_language"]
    assert registration["timezone"] == body["timezone"]
    assert "access" in token.keys()
    assert "refresh" in token.keys()


@pytest.mark.acceptance
def test_login(client, body):
    # Given
    client.post("/user/", json=body)

    # When
    response = client.post(
        "/user/login", json={"email": body["email"], "password": body["password"]}
    )
    token = response.json()["token"]

    # Then
    assert response.status_code == 200
    assert "access" in token.keys()
    assert "refresh" in token.keys()


@pytest.mark.acceptance
def test_logout(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["access"]

    # When
    response = client.post("/user/logout", headers={"Authorization": f"Bearer {token}"})

    # Then
    assert response.status_code == 204


@pytest.mark.acceptance
def test_account_exists(client, body):
    # Given
    client.post("/user/", json=body)

    # When
    response = client.post("/user/", json=body)

    assert response.status_code == 409
    assert response.json()["data"] == {"Error": "EMAIL_ALREADY_EXISTS"}


@pytest.mark.acceptance
def test_refresh_token(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["refresh"]

    # When
    response = client.post("/user/refresh", json={"refresh": token})

    # Then
    assert response.status_code == 200
    assert "access" in response.json().keys()
    assert "refresh" in response.json().keys()


@pytest.mark.acceptance
def test_delete_account(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["access"]

    # When
    response = client.delete("/user", headers={"Authorization": f"Bearer {token}"})

    # Then
    assert response.status_code == 204


@pytest.mark.acceptance
def test_account_not_found(client):
    # Given
    random_uuid = uuid4()

    # When
    response = client.get(f"/user/{random_uuid}")

    # Then
    assert response.status_code == 404
    assert response.json()["data"] == {"Error": "USER_NOT_FOUND"}


@pytest.mark.acceptance
def test_account_found(client, body):
    # Given
    user_uuid = body["uuid"]
    response = client.post("/user/", json=body)

    # When
    response = client.get(f"/user/{user_uuid}")

    # Then
    assert response.status_code == 200
    assert response.json()["name"] == body["name"]
    assert response.json()["surnames"] == body["surnames"]
    assert response.json()["timezone"] == body["timezone"]


@pytest.mark.acceptance
def test_change_password(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["access"]

    # When
    response = client.put(
        "/user/password",
        json={"password": "new_password"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 204


@pytest.mark.acceptance
def test_invalid_acces_token(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["access"]

    # When
    response = client.put(
        "/user/password",
        json={"password": "new_password"},
        headers={"Authorization": f"Bearer {token}123"},
    )

    # Then
    assert response.status_code == 401
    assert response.json()["data"] == {"Error": "INVALID_TOKEN"}


@pytest.mark.acceptance
def test_invalid_refresh_token(client, body):
    # Given
    response = client.post("/user/", json=body)
    token = response.json()["token"]["refresh"]

    # When
    response = client.post(
        "/user/refresh",
        json={"refresh": token + "123"},
    )

    # Then
    assert response.status_code == 401
    assert response.json()["data"] == {"Error": "INVALID_TOKEN"}