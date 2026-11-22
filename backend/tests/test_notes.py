from fastapi.testclient import TestClient
from datetime import datetime, timezone

from main import app

client = TestClient(app)

notes = notes = {
    "data": [
        {
            "id": 1,
            "title": "Заголовок",
            "body": "Текст заметки",
            "created_at": "2020-01-01T00:00:00Z",
            "edited_at": "2020-01-01T00:00:00Z",
            "tags": [
                { "id": 1, "name": "Тег1" },
                { "id": 2, "name": "Тег2" }
            ]
        },
        {
            "id": 2,
            "title": "Заголовок",
            "body": "Текст заметки",
            "created_at": "2020-01-01T00:00:00Z",
            "edited_at": "2020-01-01T00:00:00Z",
            "tags": []
        },
        {
            "id": 3,
            "title": "Заголовок",
            "body": "Текст заметки",
            "created_at": "2020-01-01T00:00:00Z",
            "edited_at": "2020-01-01T00:00:00Z",
            "tags": []
        }
    ],
    "total": 120,
    "offset": 0,
    "limit": 20
}

def test_read_all_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert response.json() == notes

def test_create_note():
    before = datetime.now(timezone.utc)
    response = client.post(
        "/notes/",
        json={ "title": "Test", "body": "test body" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    created_at = datetime.fromisoformat(data["created_at"])
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == "test body"
    assert before <= created_at <= after
    assert before <= edited_at <= after
    assert created_at == edited_at
    assert data["tags"] == []

def test_create_note_with_whitespaces():
    before = datetime.now(timezone.utc)
    response = client.post(
        "/notes/",
        json={ "title": "   Test    ", "body": "test body    " }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    created_at = datetime.fromisoformat(data["created_at"])
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == "test body"
    assert before <= created_at <= after
    assert before <= edited_at <= after
    assert created_at == edited_at
    assert data["tags"] == []

def test_create_note_title_empty():
    response = client.post(
        "/notes/",
        json={ "title": "   ", "body": "test body" }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at least 1 character"

def test_create_note_body_empty():
    before = datetime.now(timezone.utc)
    response = client.post(
        "/notes/",
        json={ "title": "Test", "body": "" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    created_at = datetime.fromisoformat(data["created_at"])
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == ""
    assert before <= created_at <= after
    assert before <= edited_at <= after
    assert created_at == edited_at
    assert data["tags"] == []

def test_create_note_title_null():
    response = client.post(
        "/notes/",
        json={ "title": None, "body": "test body" }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_create_note_body_null():
    before = datetime.now(timezone.utc)
    response = client.post(
        "/notes/",
        json={ "title": "Test", "body": None }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    created_at = datetime.fromisoformat(data["created_at"])
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == None
    assert before <= created_at <= after
    assert before <= edited_at <= after
    assert created_at == edited_at
    assert data["tags"] == []

def test_create_note_title_missing():
    response = client.post(
        "/notes/",
        json={ "body": "test body" }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_note_body_missing():
    before = datetime.now(timezone.utc)
    response = client.post(
        "/notes/",
        json={ "title": "Test" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    created_at = datetime.fromisoformat(data["created_at"])
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == None
    assert before <= created_at <= after
    assert before <= edited_at <= after
    assert created_at == edited_at
    assert data["tags"] == []

def test_create_note_empty_request():
    response = client.post(
        "/notes/",
        json={}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_update_note():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "title": "new title", "body": "new body" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["title"] == "new title"
    assert data["body"] == "new body"
    assert before <= edited_at <= after

def test_update_note_title_only():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "title": "new title" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["title"] == "new title"
    assert before <= edited_at <= after

def test_update_note_body_only():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "body": "new body" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["body"] == "new body"
    assert before <= edited_at <= after

def test_update_note_title_null():
    response = client.patch(
        "/notes/2",
        json={ "title": None, "body": "new body" }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_update_note_body_null():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "title": "new title", "body": None }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    edited_at = datetime.fromisoformat(data["edited_at"])
    assert response.status_code == 200
    assert before <= edited_at <= after
    assert data["id"] == 2
    assert data["title"] == "new title"
    assert data["body"] == None


def test_update_nonexistent_note():
    response = client.patch(
        "/notes/7",
        json={ "title": "new title", "body": "new body" }
    )
    assert response.status_code == 404
    assert response.json() == { "detail": "Note not found" }
