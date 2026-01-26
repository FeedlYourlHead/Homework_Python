from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import String, DateTime, create_engine, select
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

def setup_database():
    Base.metadata.create_all(engine)

def get_all_messages():
    with Session(engine) as session:
        select_messages = select(Message).order_by(Message.content)
        messages = session.scalars(select_messages).all()
        return messages

def get_all_authors():
    with Session(engine) as session:
        select_authors = select(Message).order_by(Message.author)
        authors = session.scalars(select_authors).all()
        return authors


