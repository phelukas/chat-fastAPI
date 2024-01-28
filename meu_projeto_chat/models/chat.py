# from enum import Enum
# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
# from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
# from datetime import datetime


# class Base(DeclarativeBase):
#     pass


# class MessageStatus(str, Enum):
#     sent = "sent"
#     received = "received"
#     read = "read"


# class Message(Base):
#     __tablename__ = "messages"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     content: Mapped[str] = mapped_column(Text)
#     timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     status: Mapped[MessageStatus] = mapped_column()
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

#     user: Mapped[User] = relationship("User", back_populates="messages")
