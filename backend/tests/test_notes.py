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
            "created_at": "2020-01-01T00:00:00",
            "edited_at": "2020-01-01T00:00:00",
            "tags": [
                { "id": 1, "name": "Тег1" },
                { "id": 2, "name": "Тег2" }
            ]
        },
        {
            "id": 2,
            "title": "Заголовок",
            "body": "Текст заметки",
            "created_at": "2020-01-01T00:00:00",
            "edited_at": "2020-01-01T00:00:00",
            "tags": []
        },
        {
            "id": 3,
            "title": "Заголовок",
            "body": "Текст заметки",
            "created_at": "2020-01-01T00:00:00",
            "edited_at": "2020-01-01T00:00:00",
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
    assert response.status_code == 201
    assert data["title"] == "Test"
    assert data["body"] == "test body"
    assert before <= data["created_at"] <= after
    assert before <= data["edited_at"] <= after
    assert data["created_at"] == data["edited_at"]
    assert data["tags"] == []

def test_update_note():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "title": "new title", "body": "new body" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["title"] == "new title"
    assert data["body"] == "new body"
    assert before <= data["created_at"] <= after
    assert before <= data["edited_at"] <= after

def test_update_note_title_only():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "title": "new title" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["title"] == "new title"
    assert before <= data["created_at"] <= after
    assert before <= data["edited_at"] <= after

def test_update_note_body_only():
    before = datetime.now(timezone.utc)
    response = client.patch(
        "/notes/2",
        json={ "body": "new body" }
    )
    after = datetime.now(timezone.utc)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 2
    assert data["body"] == "new body"
    assert before <= data["created_at"] <= after
    assert before <= data["edited_at"] <= after

def test_update_note_title_null():
    response = client.patch(
        "/notes/2",
        json={ "title": None, "body": "new body" }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_update_note_body_null():
    pass # TODO!

def test_update_nonexistent_note():
    response = client.patch(
        "/notes/7",
        json={ "title": "new title", "body": "new body" }
    )
    assert response.status_code == 404
    assert response.json() == { "detail": "Note not found" }
