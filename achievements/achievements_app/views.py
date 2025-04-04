from django.shortcuts import render, redirect
from .models import Achievement
from django.http import JsonResponse
from django.db import connection

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
def information(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/information.html',
                 {'achievements': achievements})

def check_user(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        login = data.get('login')
        password = data.get('password')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE login = %s AND password = %s",
                [login, password]
            )
            count = cursor.fetchone()[0]

        return JsonResponse({'exists': count > 0})

    return JsonResponse({'exists': False})