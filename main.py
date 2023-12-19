from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

import schemas
from database import get_db

#  The Base import is needed by Alembic, as it needs to import Base after models are initialized
from db_models import Base, Note  # noqa: F401
from db_query_functions import (
    create_document,
    create_note,
    create_user,
    create_user_document,
    create_user_note,
    get_document,
    get_documents,
    get_notes,
    get_user,
    get_users,
)

app = FastAPI()


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/users/{user_id}", response_model=schemas.UserNotes)
def fetch_user(user_id: int, db=Depends(get_db)):
    if not (user := get_user(db, user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.get("/users", response_model=list[schemas.UserNotes])
def fetch_users(db=Depends(get_db)):
    return get_users(db)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def add_user(user: schemas.UserBase, db=Depends(get_db)):
    return create_user(db, user)


# ** Notes ** #


@app.post("/notes", status_code=status.HTTP_201_CREATED)
def add_note(note: schemas.NoteCreate, db=Depends(get_db)):
    if not (get_user(db, note.user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return create_note(db, note)


@app.get("/notes", response_model=list[schemas.Note])
def fetch_notes(user_id: int = None, db=Depends(get_db)):
    return get_notes(db, user_id=user_id)


# ** User notes ** #


@app.get("/users/{user_id}/notes", response_model=list[schemas.Note])
def fetch_user_notes(user_id: int, db=Depends(get_db)):
    if not (user := get_user(db, user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user.notes


@app.post(
    "/users/{user_id}/notes",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def add_user_note(user_id: int, note: schemas.UserNoteCreate, db=Depends(get_db)):
    if not (user := get_user(db, user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return create_user_note(db, note, user)


# ** Documents ** #


@app.post(
    "/documents", status_code=status.HTTP_201_CREATED, response_model=schemas.Document
)
def add_document(document: schemas.DocumentBase, db=Depends(get_db)):
    return create_document(db, document)


@app.post(
    "/user-documents",
    status_code=status.HTTP_201_CREATED,
)
def add_user_document(params: schemas.UserDocument, db=Depends(get_db)):
    if not (user := get_user(db, params.user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not (document := get_document(db, params.document_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return create_user_document(db, user, document)


@app.get("/documents/{document_id}", response_model=schemas.Document)
def fetch_document(document_id: int, db=Depends(get_db)):
    if not (document := get_document(db, document_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return document


@app.get("/documents", response_model=list[schemas.Document])
def fetch_documents(db=Depends(get_db)):
    return get_documents(db)
