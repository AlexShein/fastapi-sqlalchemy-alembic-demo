from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from environment import env

host = env.DB_HOST
port = env.DB_PORT
db_name = env.DB_NAME
user = env.DB_USER
pswd = env.DB_PASS


SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{pswd}@{host}:{port}/{db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class _Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __str__(self):
        return f"<{self.__class__.__name__} id:{self.id}>"

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
