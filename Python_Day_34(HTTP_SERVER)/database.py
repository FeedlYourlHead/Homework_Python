
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Message(Base):
    """Модель для хранения капсул времени"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    author = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    unlock_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

engine = create_engine('sqlite:///capsules.db', echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db_session():
    """Возвращает новую сессию базы данных"""
    return Session()

def init_database():
    """Инициализация базы данных (создание таблиц)"""
    Base.metadata.create_all(engine)
