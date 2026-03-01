from flask import render_template, url_for, redirect, request, flash, Blueprint
from flask_login import current_user, login_required, logout_user, login_user
from forms import RegisterForm, LoginForm, AddCarForm
from extensions import db
from models import User, Car

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    cars = Car.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', cars=cars)

@main.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    form = AddCarForm()
    if form.validate_on_submit():
        car = Car(
            brand=form.brand.data,
            model=form.model.data,
            year=form.year.data.year if hasattr(form.year.data, 'year') else form.year.data,
            fuel_type=form.fuel_type.data,
            user_id=current_user.id
        )
        db.session.add(car)
        db.session.commit()
        
        flash('Автомобиль успешно добавлен!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_car.html', form=form)

@main.route('/delete_car/<int:car_id>')
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    
    if car.user_id != current_user.id:
        flash('У вас нет прав на удаление этого автомобиля', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(car)
    db.session.commit()
    
    flash('Автомобиль удален из гаража', 'success')
    return redirect(url_for('main.dashboard'))
