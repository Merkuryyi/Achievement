from django.shortcuts import render
from .models import Achievement

def autorization(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/autorization.html',
                 {'achievements': achievements})
def recovery(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/recovery.html',
                 {'achievements': achievements})
def registration(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/registration.html',
                 {'achievements': achievements})


# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Проверяем существование пользователя
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление после успешного входа
            else:
                # Пользователь не найден или пароль неверный
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()

    return render(request, 'achievements_app/login.html', {'form': form})