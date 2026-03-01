from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'main.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

# Регистрация蓝图
app.register_blueprint(main)

# Создание таблиц базы данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
