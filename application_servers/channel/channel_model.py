from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from application_servers.db.base import BaseEntity


class Channel(BaseEntity):
    __tablename__ = "channel"
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="channels")
    messages: Mapped[List["Message"]] = relationship(
        back_populates="channel", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Channel(id={super().id!r}, name={self.name!r}, description={self.description!r})"
