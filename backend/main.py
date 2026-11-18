from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import NoteCreate, NoteResponse, NoteUpdate, NotesResponseList
from datetime import datetime, timezone

app = FastAPI()

time: datetime = datetime.now(timezone.utc)
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
    ]
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
        id= 1,
        title= note.title,
        body= note.body if note.body != None else "",
        created_at= time,
        edited_at= time,
        tags= []
        )
    return res

@app.patch("/notes/{note_id}")
async def update_note(note_id: int, note: NoteUpdate) -> NoteResponse: #Placeholder
    time: datetime = datetime.now(timezone.utc)
    try:
        for n in notes["data"]:
            if n["id"] == note_id:
                stored_item_data = n
                stored_item_model = NoteResponse(**stored_item_data)
                update_data = note.model_dump(exclude_unset=True)
                if update_data: stored_item_model.edited_at = time
                updated_item = stored_item_model.model_copy(update=update_data)
                n = jsonable_encoder(updated_item)
                return updated_item
    except IndexError:
        raise HTTPException(404, "Note not found")
    raise HTTPException(404, "Note not found")
