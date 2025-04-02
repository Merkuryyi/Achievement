from django.db import models

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.core.exceptions import ValidationError
from django.db import models
import re

def validate_phone(value):
    pattern = r'^(\+7|8)[\d\- ]{10,15}$'
    if not re.match(pattern, value):
        raise ValidationError('Неверный формат телефона')

class UserProfile(models.Model):
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone],
        help_text="Формат: +79991234567 или 89991234567"
    )