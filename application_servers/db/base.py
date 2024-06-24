from application_servers.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from flask import current_app as app

# Create a base class
Base = declarative_base()


# Database connection string for PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@{app.config["DB_HOST"]}:{app.config["DB_PORT"]}/{app.config["DB_NAME"]}"
)

# Create engine and session
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create the tables in the database
Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseAccessor:
    def __init__(self, entity):
        self.entity = entity

    def add(self, obj):
        with session_scope() as session:
            session.add(obj)

    def get(self, **kwargs):
        with session_scope() as session:
            return session.query(self.entity).filter_by(**kwargs).first()

    def count(self, **kwargs):
        with session_scope() as session:
            return session.query(self.entity).filter_by(**kwargs).count()

    def get_all_paginated(self, offset=0, limit=10, **kwargs):
        with session_scope() as session:
            return session.query(self.entity).filter_by(**kwargs).offset(offset).limit(limit).all()
    
    def get_all(self, **kwargs):
        with session_scope() as session:
            return session.query(self.entity).filter_by(**kwargs).all()

    def update(self, id, data):
        with session_scope() as session:
            obj = session.query(self.entity).filter_by(id=id).first()
            for key, value in data.items():
                setattr(obj, key, value)
            session.add(obj)

    def delete(self, **kwargs):
        with session_scope() as session:
            obj = session.query(self.entity).filter_by(**kwargs).first()
            session.delete(obj)




class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)