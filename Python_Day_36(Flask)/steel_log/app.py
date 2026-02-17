# НЕ ДОДЕЛАНО!!!!
from flask_sqlalchemy import  SQLAlchemy 
from flask import render_template, request, redirect, url_for, Flask
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'workouts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Workout {self.reps}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        reps = request.form.get('reps')

        if reps and reps.isdigit() and int(reps) > 0:

            new_workout = Workout(reps=int(reps))
            db.session.add(new_workout)
            db.session.commit()

        return redirect(url_for('index'))

    workouts = Workout.query.order_by(Workout.date.desc()).all()

    total_reps = sum(workout.reps for workout in workouts)

    return render_template('index.html', workouts=workouts, total_reps=total_reps)

    



    
if __name__ == '__main__':
    app.run(debug=True)


