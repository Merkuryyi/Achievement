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
def editPhone(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/editPhone.html',
                 {'achievements': achievements})
def confirmation(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/confirmation.html',
                 {'achievements': achievements})
def notification(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/notification.html',
                 {'achievements': achievements})
def check_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login = data.get('login')
        password = data.get('password')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT phone FROM users WHERE login = %s AND password = %s",
                [login, password]
            )
            row = cursor.fetchone()

        if row:
            return JsonResponse({'exists': row})
        else:
            return JsonResponse({'exists': False})

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
            photoLink = data.get('photoLink')

            with connection.cursor() as cursor:
                cursor.execute("insert into users (login, password, phone, email, photo) values (%s, %s, %s, %s, %s)",
                [login, password, phone, email, photoLink])
            id = get_user_id_by_phone(phone)
            with connection.cursor() as cursor:
                cursor.execute("insert into status_users (user_id, status, date) values (%s, %s, now())",
                               [id, status])
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
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        login = (data.get('login') or '').strip()
        lastname = (data.get('lastName') or '').strip()
        firstname = (data.get('firstName') or '').strip()
        patronymic = (data.get('patronymic') or '').strip()
        photo = (data.get('photo') or '').strip()
        phone = (data.get('phone') or '').strip()

        user_id = get_user_id_by_phone(phone)
        if not user_id:
            return JsonResponse({'error': 'User not found'}, status=404)

        with connection.cursor() as cursor:
            if login:
                cursor.execute(
                    "UPDATE users SET login = %s WHERE user_id = %s",
                    [login, user_id]
                )
            if photo:
                cursor.execute(
                    "UPDATE users SET photo = %s WHERE user_id = %s",
                    [photo, user_id]
                )
            if lastname:
                cursor.execute(
                    "UPDATE additional_information_users SET lastname = %s WHERE user_id = %s",
                    [lastname, user_id]
                )
            if firstname:
                cursor.execute(
                    "UPDATE additional_information_users SET firstname = %s WHERE user_id = %s",
                    [firstname, user_id]
                )
            if patronymic:
                cursor.execute(
                    "UPDATE additional_information_users SET patronymic = %s WHERE user_id = %s",
                    [patronymic, user_id]
                )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def editLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login = data.get('login')
        phone = data.get('phone')
    try:
        data = json.loads(request.body)

        user_id = get_user_id_by_phone(phone)
        if not data['login'].strip():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET login = %s WHERE user_id = %s",
                    [login, user_id]
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
            email = data.get('email')

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET email = %s WHERE phone = %s",
                    [email, phone]
                )
    return JsonResponse({'success': True})
def phoneReset(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone = data.get('phone')
            login = data.get('login')

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET phone = %s WHERE login = %s",
                    [phone, login]
                )
    return JsonResponse({'success': True})


def statusReset(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone = data.get('phone')
            user_id = get_user_id_by_phone(phone)
            status = data.get('status')
            with connection.cursor() as cursor:
                cursor.execute(
                    "update status_users set status = %s, date = now() where user_id = %s",
                    [status, user_id]
                )
    return JsonResponse({'success': True})

def check_status(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "select status from status_users inner join users on users.user_id = status_users.user_id where phone = %s",
                [phone]
            )
            status = cursor.fetchone()[0]
            return JsonResponse({'status': status})

        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def check_isActiveNotification(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "select activeNotification from users where phone = %s",
                [phone]
            )
            notification = cursor.fetchone()[0]
            return JsonResponse({'notification': notification})

        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def editActiveNotification(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        isActiveNotification = data.get('isActiveNotification')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "update users set activeNotification = %s where phone = %s",
                [isActiveNotification, phone]
            )
            return JsonResponse({'success': True})

        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def countNotification(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "select count(*) from Notification inner join users on users.user_id =  Notification.user_id"
                " where phone = %s and is_read = 'false'",
                [phone]
            )
            count = cursor.fetchone()[0]
            return JsonResponse({'count': count})

        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def returnNotification(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, DATE_TRUNC('second', notification.created_at)::time "
                "AS created_at FROM notification "
                "INNER JOIN users ON users.user_id = notification.user_id WHERE users.phone = %s "
                "AND notification.is_read = false order by created_at desc;",
                [phone]
            )

            notifications = cursor.fetchall()

            result = [
                {
                    'id': row[0],
                    'title': row[1],
                    'created_at': row[2]
                }
                for row in notifications
            ]

            return JsonResponse({'notifications': result}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def editStatusNotification(request):
    try:
        data = json.loads(request.body)
        id = data.get('id')

        with connection.cursor() as cursor:
            cursor.execute(
                "update notification set is_read = true where id = %s",
                [id]
            )
            return JsonResponse({'success': True})


    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def createNotification(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        user_id = get_user_id_by_phone(phone)
        text = data.get('text')
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into notification "
                "(user_id, created_at, is_read, title) values (%s, now(), false, %s)",
                [user_id, text]
            )
            return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def returnAchievement(request):
    try:
        data = json.loads(request.body)
        isFiltered = data.get('isFiltered')

        with connection.cursor() as cursor:
            if isFiltered == 'false':
                cursor.execute(
                "SELECT "
                    "users.login, "
                    "achievement.achievement_id, "
                    "achievement.title, "
                    "achievement.date, "
                    "achievement.photo, "
                    "COALESCE(comment_counts.count_comment, 0) AS count_comment, "
                    "COALESCE(like_counts.count_like, 0) AS count_like "
                "FROM achievement "
                "INNER JOIN users ON achievement.user_id = users.user_id "
                "LEFT JOIN (SELECT achievement_id, COUNT(*) AS count_comment FROM comment GROUP BY achievement_id) "
                "AS comment_counts ON achievement.achievement_id = comment_counts.achievement_id "
                "LEFT JOIN (SELECT achievement_id, COUNT(*) AS count_like FROM achievement_like GROUP BY achievement_id) "
                "AS like_counts ON achievement.achievement_id = like_counts.achievement_id "
                "WHERE now() > achievement.date - interval '1 month' "
                "ORDER BY achievement.date ASC; ",
            )

            achievements = cursor.fetchall()
            result = [
                {
                    'login': row[0],
                    'id_achievement': row[1],
                    'title': row[2],
                    'date': row[3],
                    'photoLink': row[4],
                    'countComment': row[5],
                    'countLike': row[6]
                }
                for row in achievements
            ]
            return JsonResponse({'achievements': result}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def newLike(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        user_id = get_user_id_by_phone(phone)
        achievement_id = data.get('achievement_id')
        print(achievement_id)

        with connection.cursor() as cursor:
            cursor.execute(
                "insert into achievement_like (achievement_id, user_id) values (%s, %s)",
                [achievement_id, user_id]
            )
            return JsonResponse({'success': True})


    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def deleteLike(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        user_id = get_user_id_by_phone(phone)
        achievement_id = data.get('achievement_id')

        with connection.cursor() as cursor:
            cursor.execute(
                "delete from achievement_like where achievement_id = %s and user_id = %s",
                [achievement_id, user_id]
            )
            return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def check_Like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        user_id = get_user_id_by_phone(phone)
        achievement_id = data.get('achievement_id')

        with connection.cursor() as cursor:
            cursor.execute(
                "select * from achievement_like WHERE user_id = %s AND achievement_id = %s",
                [user_id, achievement_id]
            )
            row = cursor.fetchone()

        if row:
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})

    return JsonResponse({'exists': False})


def photoUser(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        cursor = connection.cursor()
        try:
            cursor.execute(
                "select photo from users WHERE phone = %s",
                [phone]
            )
            link = cursor.fetchone()[0]
            return JsonResponse({'photo': link})
        finally:
            cursor.close()

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

