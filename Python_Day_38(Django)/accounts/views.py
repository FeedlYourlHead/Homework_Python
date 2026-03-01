from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')
