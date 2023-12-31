from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, select
from sqlalchemy.orm import column_property, relationship

from database import Base


class User(Base):
    email = Column(
        String,
        unique=True,
    )
    is_active = Column(Boolean, default=True)
    # You can play with different lazy=... options, such as
    # subquery, selectin, raise, ...
    notes = relationship("Note", back_populates="user", lazy="selectin")


class Note(Base):
    title = Column(
        String,
    )
    description = Column(
        String,
    )
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="notes")


class Document(Base):
    title = Column(
        String,
    )
    content = Column(
        String,
    )
    users = relationship(
        "User",
        secondary="userdocument",
        secondaryjoin="and_(User.is_active == True, UserDocument.user_id == User.id)",
    )
    total_users = column_property(select(0).scalar_subquery())

    @classmethod
    def __declare_last__(cls):
        cls.total_users = column_property(
            select(func.count(UserDocument.user_id))
            .select_from(UserDocument)
            .filter(UserDocument.document_id == cls.id)
            .scalar_subquery()
        )


class UserDocument(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    document_id = Column(Integer, ForeignKey("document.id"))
