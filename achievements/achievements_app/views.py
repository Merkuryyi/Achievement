from django.shortcuts import render
from .models import Achievement

def achievement_autorization(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/autorization.html',
                 {'achievements': achievements})

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello! This is Achievements app. Add /admin to manage achievements.")

