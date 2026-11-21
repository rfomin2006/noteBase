from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import NoteCreate, NoteResponse, NoteUpdate, NotesResponseList
from datetime import datetime, timezone

app = FastAPI()

notes = { # Placeholder data
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

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.get("/notes/")
async def read_notes() -> NotesResponseList: # Placeholder
    return NotesResponseList.model_validate(notes)

@app.post("/notes/", status_code=201)
async def create_note(note: NoteCreate) -> NoteResponse: # Placeholder
    time: datetime = datetime.now(timezone.utc)
    res: NoteResponse = NoteResponse(
        id=1,
        title=note.title,
        body=note.body,
        created_at=time,
        edited_at=time,
        tags= []
        )
    return res

@app.patch("/notes/{note_id}")
async def update_note(note_id: int, note: NoteUpdate) -> NoteResponse: #Placeholder
    time: datetime = datetime.now(timezone.utc)
    for index, n in enumerate(notes["data"]):
        if n["id"] == note_id:
            stored_item_data = n
            stored_item_model = NoteResponse(**stored_item_data)
            update_data = note.model_dump(exclude_unset=True)
            if update_data: stored_item_model.edited_at = time
            updated_item = NoteResponse.model_validate({**stored_item_model.model_dump(), **update_data})
            notes["data"][index] = jsonable_encoder(updated_item)
            return updated_item
    raise HTTPException(404, "Note not found")
