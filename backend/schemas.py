from pydantic import BaseModel, MISSING
from pydantic.types import StringConstraints
from typing import Annotated, TypeAlias
from datetime import datetime

TitleStr: TypeAlias = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
StrippedStr: TypeAlias = Annotated[str, StringConstraints(strip_whitespace=True)]

class NoteCreate(BaseModel):
    title: TitleStr
    body: StrippedStr | None = None

class TagResponse(BaseModel):
    id: int
    name: str

class NoteResponse(BaseModel):
    id: int
    title: TitleStr
    body: StrippedStr | None
    created_at: datetime
    edited_at: datetime
    tags: list[TagResponse]

class NoteUpdate(BaseModel):
    title: TitleStr | MISSING = MISSING
    body: StrippedStr | None = None

class NotesResponseList(BaseModel):
    data: list[NoteResponse]
