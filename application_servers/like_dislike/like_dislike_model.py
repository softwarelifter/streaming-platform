from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from application_servers.db.base import BaseEntity


class VideoLikeDislike(BaseEntity):
    __tablename__ = "video_like_dislike"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="like_dislikes")
    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"))
    video: Mapped["Video"] = relationship(back_populates="like_dislikes")
    like: Mapped[Optional[bool]]
    dislike: Mapped[Optional[bool]]

    def __repr__(self) -> str:
        return f"VideoLikeDislike(id={super().id!r}, like={self.like!r}, dislike={self.dislike!r})"


class CommentLikeDislike(BaseEntity):
    __tablename__ = "commnent_like_dislike"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="like_dislikes")
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"))
    comment: Mapped["Comment"] = relationship(back_populates="like_dislikes")
    like: Mapped[Optional[bool]]
    dislike: Mapped[Optional[bool]]

    def __repr__(self) -> str:
        return f"CommentLikeDislike(id={super().id!r}, like={self.like!r}, dislike={self.dislike!r})"
