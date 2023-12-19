from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from db_models import Document, Note, User
from schemas import DocumentBase, NoteCreate, UserBase, UserNoteCreate


def get_user(db: Session, user_id: int) -> User | None:
    return db.execute(select(User).filter(User.id == user_id)).scalars().first()


def get_users(db: Session) -> list[User]:
    return db.execute(select(User)).scalars().all()


def create_user(db: Session, user: UserBase) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_notes(db: Session, user_id: int = None) -> list[Note]:
    query = select(Note)
    if user_id:
        query = query.filter(Note.user_id == user_id)
    return db.execute(query).scalars().all()


def create_user_note(db: Session, note: UserNoteCreate, user: User) -> User:
    user.notes.append(Note(**note.model_dump()))
    db.commit()
    db.refresh(user)
    return user


def create_note(db: Session, note: NoteCreate) -> Note:
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def create_document(db: Session, document: DocumentBase) -> Document:
    db_document = Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents(db: Session) -> list[Document]:
    return (
        db.execute(select(Document).options(selectinload(Document.users)))
        .scalars()
        .all()
    )


def get_document(db: Session, document_id: int) -> Document | None:
    return (
        db.execute(select(Document).filter(Document.id == document_id))
        .scalars()
        .first()
    )


def create_user_document(db: Session, user: User, document: Document) -> None:
    document.users.append(user)
    db.commit()
    return
