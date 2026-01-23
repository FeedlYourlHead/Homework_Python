from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, create_engine
import datetime


class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    unlock_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

DB_URL = 'sqlite:///messages.db'
engine = create_engine(DB_URL, echo=True)

def set_message():
    pass

