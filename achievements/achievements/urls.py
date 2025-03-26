from django.contrib import admin
from django.urls import path, include
from achievements_app import views  # Убедитесь, что achievements_app существует
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.achievement_list, name='achievement_list'),
]

