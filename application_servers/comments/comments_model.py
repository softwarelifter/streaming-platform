from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from application_servers.db.base import BaseEntity


class Comment(BaseEntity):
    __tablename__ = "comment"
    text: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comments")
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"))
    video: Mapped["Video"] = relationship(back_populates="comments")
    likes_count: Mapped[int] = mapped_column(Integer)
    dislikes_count: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Comment(id={super().id!r}, text={self.text!r})"
