from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Стандартная админка Django
    path('', views.achievement_list, name='achievement_list'),  # Главная страница
]
