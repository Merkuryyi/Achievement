from django.shortcuts import render, redirect
from .models import Achievement
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db import connection
import json
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


import traceback


def passwordReset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login = data.get('login')
            password = data.get('password')

            if not login or not password:
                return JsonResponse({'error': 'Логин и пароль обязательны'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password = %s WHERE login = %s",
                    [password, login]
                )
                if cursor.rowcount == 0:
                    return JsonResponse({'error': 'Пользователь не найден'}, status=404)

            return JsonResponse({'success': True})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)