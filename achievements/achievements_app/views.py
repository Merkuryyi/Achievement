from django.shortcuts import render
from .models import Achievement

def achievement_list(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements_app/list.html',
                 {'achievements': achievements})

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello! This is Achievements app. Add /admin to manage achievements.")

