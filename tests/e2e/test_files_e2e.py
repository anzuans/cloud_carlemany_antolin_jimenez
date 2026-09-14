import io
import os
import time
import uuid

import pytest
import requests
from pypdf import PdfWriter

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


def register_and_login() -> tuple[dict[str, str], int]:
    email = f"files-e2e-{uuid.uuid4().hex}@example.com"
    password = "secret-password"

    register_response = requests.post(
        f"{BASE_URL}/authentication/register",
        json={"email": email, "password": password},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert register_response.status_code == 200

    login_response = requests.post(
        f"{BASE_URL}/authentication/login",
        json={"email": email, "password": password},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert login_response.status_code == 200
    headers = {"auth": login_response.json()["token"]}

    introspect_response = requests.get(
        f"{BASE_URL}/authentication/introspect",
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert introspect_response.status_code == 200
    return headers, introspect_response.json()["user_id"]


def pdf_content() -> bytes:
    output = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(output)
    return output.getvalue()


def create_file(headers: dict[str, str], title: str, description: str) -> int:
    response = requests.post(
        f"{BASE_URL}/files",
        headers=headers,
        json={"title": title, "description": description},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert response.status_code == 200
    return response.json()["id"]


def upload_pdf(headers: dict[str, str], file_id: int, filename: str) -> None:
    response = requests.post(
        f"{BASE_URL}/files/{file_id}",
        headers=headers,
        files={"content": (filename, pdf_content(), "application/pdf")},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.e2e
def test_files_workflow() -> None:
    owner_headers, owner_user_id = register_and_login()
    other_user_headers, _ = register_and_login()

    empty_list_response = requests.get(
        f"{BASE_URL}/files", headers=owner_headers, timeout=REQUEST_TIMEOUT_SECONDS
    )
    assert empty_list_response.status_code == 200
    assert empty_list_response.json() == []

    first_file_id = create_file(owner_headers, "first", "First PDF")
    first_file_response = requests.get(
        f"{BASE_URL}/files/{first_file_id}",
        headers=owner_headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert first_file_response.status_code == 200
    assert first_file_response.json() == {
        "id": first_file_id,
        "title": "first",
        "description": "First PDF",
        "content_path": None,
        "original_filename": None,
        "user_id": owner_user_id,
    }

    upload_pdf(owner_headers, first_file_id, "first.pdf")
    second_file_id = create_file(owner_headers, "second", "Second PDF")
    upload_pdf(owner_headers, second_file_id, "second.pdf")

    forbidden_response = requests.get(
        f"{BASE_URL}/files/{first_file_id}",
        headers=other_user_headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert forbidden_response.status_code == 403
    assert forbidden_response.json() == {"detail": "Forbidden"}

    merge_response = requests.post(
        f"{BASE_URL}/files/merge",
        headers=owner_headers,
        json={"file_ids": [first_file_id, second_file_id]},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert merge_response.status_code == 200
    merged_file_id = merge_response.json()["id"]

    merged_file_response = requests.get(
        f"{BASE_URL}/files/{merged_file_id}",
        headers=owner_headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert merged_file_response.status_code == 200
    merged_file = merged_file_response.json()
    assert merged_file["title"] == "first_second_merged"
    assert merged_file["description"] == "Merged file from 2 files"
    assert merged_file["original_filename"] == "first_second_merged.pdf"
    assert merged_file["content_path"]

    list_response = requests.get(
        f"{BASE_URL}/files", headers=owner_headers, timeout=REQUEST_TIMEOUT_SECONDS
    )
    assert list_response.status_code == 200
    assert {file["id"] for file in list_response.json()} == {
        first_file_id,
        second_file_id,
        merged_file_id,
    }

    for file_id in (first_file_id, second_file_id, merged_file_id):
        delete_response = requests.delete(
            f"{BASE_URL}/files/{file_id}",
            headers=owner_headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        assert delete_response.status_code == 200
        assert delete_response.json() == {"status": "ok"}

    deleted_file_response = requests.get(
        f"{BASE_URL}/files/{first_file_id}",
        headers=owner_headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert deleted_file_response.status_code == 404
    assert deleted_file_response.json() == {"detail": "File not found"}

    final_list_response = requests.get(
        f"{BASE_URL}/files", headers=owner_headers, timeout=REQUEST_TIMEOUT_SECONDS
    )
    assert final_list_response.status_code == 200
    assert final_list_response.json() == []
