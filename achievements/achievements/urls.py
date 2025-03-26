from django.contrib import admin
from django.urls import path, include
from achievements_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.achievement_autorization, name='achievement_list'),
]

