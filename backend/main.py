from fastapi import FastAPI
from schemas import NoteCreate, NoteResponse
from datetime import datetime, timezone

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/notes/", status_code=201)
async def create_note(note: NoteCreate) -> NoteResponse:
    time: datetime = datetime.now(timezone.utc)
    res: NoteResponse = NoteResponse(
        title=note.title,
        body=note.body,
        id=1,
        created_at=time,
        edited_at=time
        )
    return res
