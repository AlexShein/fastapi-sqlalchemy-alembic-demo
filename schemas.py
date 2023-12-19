from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    description: str


class NoteCreate(NoteBase):
    user_id: int


class UserNoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    is_active: bool


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserNotes(User):
    notes: list[Note] = []

    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    title: str
    content: str


class Document(DocumentBase):
    id: int
    users: list[User] = []
    total_users: int

    class Config:
        from_attributes = True


class UserDocument(BaseModel):
    user_id: int
    document_id: int
