from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NotesResponseList,
    TagCreate,
    TagUpdate,
    TagResponse,
    TagResponseList,
)
from datetime import datetime, timezone

app = FastAPI()

notes = { # Placeholder data, identical with /tests/test_notes.py
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

tags = {
    "data": [
        { "id": 1, "name": "Tag1" },
        { "id": 2, "name": "Tag2" }
    ]
}

@app.get("/notes/{note_id}")
async def read_note(note_id: int) -> NoteResponse: # Placeholder
    for n in notes["data"]:
        if n["id"] == note_id: return NoteResponse.model_validate(n)
    raise HTTPException(404, "Note not found")

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

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    pass # TODO on database integration

@app.get("/tags/")
async def read_tags() -> TagResponseList: # Placeholder
    return TagResponseList.model_validate(tags)

@app.get("/tags/{tag_id}")
async def read_tag(tag_id: int) -> TagResponse: # Placeholder
    for tag in tags["data"]:
        if tag["id"] == tag_id: return TagResponse.model_validate(tag)
    raise HTTPException(404, "Tag not found")

@app.post("/tags/")
async def create_tag(tag: TagCreate) -> TagResponse: # Placeholder
    return TagResponse(id=1, name=tag.name)

@app.patch("/tags/{tad_id}")
async def update_tag(tag_id: int, tag: TagResponse) -> TagUpdate:
    for index, tag in enumerate(tags["data"]):
        if tag["id"] == tag_id:
            stored_item_data = tag
            stored_item_model = TagResponse(**stored_item_data)
            update_data = tag.model_dump(exclude_unset=True)
            updated_item = TagResponse.model_validate({ **stored_item_model.model_dump(), **update_data })
            tags["data"][index] = jsonable_encoder(updated_item)
            return updated_item
    raise HTTPException(404, "Tag not found")

@app.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int):
    pass # TODO on database integration
