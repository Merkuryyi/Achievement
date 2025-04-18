from django.shortcuts import render, redirect
from .models import Achievement
from django.http import JsonResponse
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
def mainPage(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/mainPage.html',
                 {'achievements': achievements})
def userInformation(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/userInformation.html',
                 {'achievements': achievements})
def editPassword(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/editPassword.html',
                 {'achievements': achievements})
def panel(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/panel.html',
                 {'achievements': achievements})
def check_user(request):
    if request.method == 'POST':
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


def check_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login = data.get('login')

        with connection.cursor() as cursor:
            cursor.execute(
                "select COUNT(login) from users where login = %s",
                [login]
            )
            count = cursor.fetchone()[0]

        return JsonResponse({'exists': count == 1})

    return JsonResponse({'exists': False})

def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        with connection.cursor() as cursor:
            cursor.execute(
                "select COUNT(email) from users where email = %s",
                [email]
            )
            count = cursor.fetchone()[0]

        return JsonResponse({'exists': count == 1})

    return JsonResponse({'exists': False})
def check_phone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')

        with connection.cursor() as cursor:
            cursor.execute(
                "select COUNT(phone) from users where phone = %s",
                [phone]
            )
            count = cursor.fetchone()[0]

        return JsonResponse({'exists': count == 1})

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

def registerUser(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')
            login = data.get('login')
            status = "active"
            lastname = data.get('lastName')
            firstname = data.get('firstName')
            patronymic = data.get('patronymic')
            with connection.cursor() as cursor:
                cursor.execute("insert into users (login, password, phone, email, status) values (%s, %s, %s, %s, %s)",
                [login, password, phone, email, status])
            with connection.cursor() as cursor1:
                cursor1.execute(
                    "select user_id from users where phone = %s",
                    [phone]
                )
                id = cursor1.fetchone()[0]

            with connection.cursor() as cursor:
                cursor.execute("insert into additional_information_users (user_id, lastname, firstname, patronymic) values (%s, %s, %s, %s)",
                [id, lastname, firstname, patronymic])
    return JsonResponse({'success': True})


def editUserInformation(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone = data.get('phone')
            login = data.get('login')
            lastname = data.get('lastName')
            firstname = data.get('firstName')
            patronymic = data.get('patronymic')

            with connection.cursor() as cursor1:
                cursor1.execute(
                    "select user_id from users where phone = %s",
                    [phone]
                )
                id = cursor1.fetchone()[0]


            with connection.cursor() as cursor:
                cursor.execute("update users set login = %s where user_id = %s",
                [login, id])

            with connection.cursor() as cursor:
                cursor.execute("update additional_information_users set lastname = %s, firstname = %s, patronymic = %s where user_id = %s",
                [lastname, firstname, patronymic, id])

    return JsonResponse({'success': True})




