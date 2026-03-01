from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class AddCarForm(FlaskForm):
    brand = StringField('Марка', validators=[DataRequired(), Length(max=30)])
    model = StringField('Модель', validators=[DataRequired(), Length(max=30)])
    year = DateField('Год выпуска', validators=[DataRequired()], format='%Y')
    fuel_type = SelectField('Тип топлива', 
                          choices=[('бензин', 'Бензин'), 
                                  ('дизель', 'Дизель'), 
                                  ('электро', 'Электро')],
                          validators=[DataRequired()])
    submit = SubmitField('Добавить автомобиль')
