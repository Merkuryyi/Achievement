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
def mainPageProfile(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/mainPageProfile.html',
                 {'achievements': achievements})

def noProfile(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/noProfile.html',
                 {'achievements': achievements})
def myAchievement(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/myAchievement.html',
                 {'achievements': achievements})
def securityProfile(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/securityProfile.html',
                 {'achievements': achievements})
def editEmail(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/editEmail.html',
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

def passwordReset(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone = data.get('phone')
            password = data.get('password')

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password = %s WHERE phone = %s",
                    [password, phone]
                )
    return JsonResponse({'success': True})

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


def get_user_id_by_phone(phone):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM users WHERE phone = %s",
            [phone]
        )
        result = cursor.fetchone()
        return result[0] if result else None


def editUserInformation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        login = data.get('login')
        lastname = data.get('lastName')
        firstname = data.get('firstName')
        patronymic = data.get('patronymic')
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        user_id = get_user_id_by_phone(phone)

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET login = %s WHERE user_id = %s",
                [login, user_id]
            )

            cursor.execute(
                "UPDATE additional_information_users "
                "SET lastname = %s, firstname = %s, patronymic = %s WHERE user_id = %s",
                [lastname, firstname, patronymic]
            )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def scoreUser(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM achievement "
                "INNER JOIN users ON achievement.user_id = users.user_id "
                "WHERE phone = %s",
                [phone]
            )
            score = cursor.fetchone()[0]
            return JsonResponse({'score': score})
        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def check_password(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        passwordInput = data.get('password')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT password FROM users where phone = %s",
                [phone]
            )
            password = cursor.fetchone()[0]

            if password == passwordInput:
                return JsonResponse({'valid': True})
            else:
                return JsonResponse({'valid': False})


        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def loginUser(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT login FROM users WHERE phone = %s",
                [phone]
            )
            login = cursor.fetchone()[0]
            return JsonResponse({'login': login})
        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def emailReset(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone = data.get('phone')
            password = data.get('password')

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password = %s WHERE phone = %s",
                    [password, phone]
                )
    return JsonResponse({'success': True})




