from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    body: str | None = None

class TagResponse(BaseModel):
    id: int
    name: str

class NoteResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    edited_at: datetime
    tags: list[TagResponse]

class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None

class NotesResponseList(BaseModel):
    data: list[NoteResponse]
