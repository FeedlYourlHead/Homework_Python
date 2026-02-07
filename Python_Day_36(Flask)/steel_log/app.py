from flask_sqlalchemy import  SQLAlchemy, Integer
from flask import render_template, request, Flask

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")


class Workouts(db.Model):
    pass

    


