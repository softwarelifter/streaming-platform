from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from application_servers.db.base import BaseEntity

from application_servers.channel.channel_model import Channel


class Video(BaseEntity):
    __tablename__ = "video"
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship(back_populates="videos")
    likes_count: Mapped[int] = mapped_column(Integer)
    dislikes_count: Mapped[int] = mapped_column(Integer)
    views_count: Mapped[int] = mapped_column(Integer)
    video_uri: Mapped[str] = mapped_column(String(100))
    privacy_level: Mapped[int] = mapped_column(Integer)
    default_language: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Video(id={super().id!r}, name={self.name!r}, description={self.description!r})"
