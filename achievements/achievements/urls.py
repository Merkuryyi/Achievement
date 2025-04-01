from django.contrib import admin
from django.urls import path
from achievements_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autorization/', views.autorization, name='autorization'),
    path('recovery/', views.recovery, name='recovery'),
path('registration/', views.registration, name='registration'),
path('check_user/', views.check_user, name='check_user'),
]