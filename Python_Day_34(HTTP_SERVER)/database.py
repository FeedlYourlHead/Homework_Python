from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    unlock_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def is_unlocked(self):
        return datetime.datetime.utcnow().date() >= self.unlock_date



