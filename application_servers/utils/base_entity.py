from sqlalchemy import declarative_base

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
