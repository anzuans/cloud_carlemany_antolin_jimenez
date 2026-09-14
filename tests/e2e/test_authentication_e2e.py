import os
import time
import uuid

import pytest
import requests

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:8000").rstrip("/")
REQUEST_TIMEOUT_SECONDS = 5
SERVICE_START_TIMEOUT_SECONDS = 30


@pytest.fixture(scope="session", autouse=True)
def wait_for_service() -> None:
    deadline = time.monotonic() + SERVICE_START_TIMEOUT_SECONDS

    while time.monotonic() < deadline:
        try:
            response = requests.get(
                f"{BASE_URL}/healthcheck", timeout=REQUEST_TIMEOUT_SECONDS
            )
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass

        time.sleep(0.5)

    pytest.fail(f"Service at {BASE_URL} did not become ready")


@pytest.mark.e2e
def test_authentication_workflow() -> None:
    email = f"e2e-{uuid.uuid4().hex}@example.com"
    registration = {
        "email": email,
        "password": "secret-password",
        "address": "Dublin",
    }

    healthcheck_response = requests.get(
        f"{BASE_URL}/healthcheck", timeout=REQUEST_TIMEOUT_SECONDS
    )
    assert healthcheck_response.status_code == 200
    assert healthcheck_response.json() == {"status": "ok"}

    register_response = requests.post(
        f"{BASE_URL}/authentication/register",
        json=registration,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert register_response.status_code == 200
    assert register_response.json() == {"status": "ok"}

    duplicate_register_response = requests.post(
        f"{BASE_URL}/authentication/register",
        json=registration,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert duplicate_register_response.status_code == 400
    assert duplicate_register_response.json() == {"detail": "Email already registered"}

    invalid_login_response = requests.post(
        f"{BASE_URL}/authentication/login",
        json={"email": email, "password": "wrong-password"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert invalid_login_response.status_code == 403
    assert invalid_login_response.json() == {"detail": "Forbidden"}

    login_response = requests.post(
        f"{BASE_URL}/authentication/login",
        json={"email": email, "password": registration["password"]},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    assert token

    headers = {"auth": token}
    introspect_response = requests.get(
        f"{BASE_URL}/authentication/introspect",
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert introspect_response.status_code == 200
    introspection = introspect_response.json()
    assert introspection["user_id"]
    assert introspection["email"] == email
    assert introspection["address"] == registration["address"]

    logout_response = requests.post(
        f"{BASE_URL}/authentication/logout",
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert logout_response.status_code == 200
    assert logout_response.json() == {"detail": "Logout endpoint"}

    revoked_token_response = requests.get(
        f"{BASE_URL}/authentication/introspect",
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert revoked_token_response.status_code == 403
    assert revoked_token_response.json() == {"detail": "Forbidden"}
