from flask import Flask, render_template, request, redirect, url_for 
from database import db, Message
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capsules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.create_all()

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/create', method=['GET', 'POST'])
def create_capsule():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        unlock_date_str = request.form.get('unlock_date')


        if not author or not content or not unlock_date_str:
            return 'Все поля должны быть заполнены', 400

        
        try:
            unlock_date = datetime.strptime(unlock_date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Неверный формат даты", 400

        new_message = Message(author=author, content=content, unlock_date=unlock_date)

        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True,port=8000)

