# НЕ ДОДЕЛАНО!!!!


from flask_sqlalchemy import  SQLAlchemy 
from flask import render_template, request, Flask
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()

@app.route('/')
def index():
    return render_template("index.html")


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    


