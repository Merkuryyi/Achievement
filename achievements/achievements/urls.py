from django.contrib import admin
from django.urls import path
from achievements_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autorization/', views.autorization, name = 'autorization'),
    path('recovery/', views.recovery, name = 'recovery'),
    path('registration/', views.registration, name = 'registration'),
    path('check_user/', views.check_user, name = 'check_user'),
    path('information/', views.information, name = 'information'),
    path('passwordReset/', views.passwordReset, name = 'passwordReset'),
    path('registerUser/', views.registerUser, name = 'registerUser'),
    path('check_login/', views.check_login, name = 'check_login'),
    path('check_phone/', views.check_phone, name = 'check_phone'),
    path('check_email/', views.check_email, name = 'check_email'),
    path('editUserInformation/', views.editUserInformation, name = 'editUserInformation'),
    path('', views.mainPage, name = 'mainPage'),
    path('userInformation/', views.userInformation, name = 'userInformation'),
    path('panel/', views.panel, name = 'panel'),
    path('editPassword/', views.editPassword, name = 'editPassword'),
    path('scoreUser/', views.scoreUser, name = 'scoreUser'),
path('check_password/', views.check_password, name = 'check_password'),
path('mainPageProfile/', views.mainPageProfile, name = 'mainPageProfile'),
]