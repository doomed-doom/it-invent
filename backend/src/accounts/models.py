from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
        ("user", "Пользователь"),
    ]

    Роль = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    Имя = models.CharField(max_length=100, blank=True)
    Фамилия = models.CharField(max_length=100, blank=True)
    Отчество = models.CharField(max_length=100, blank=True)
    Организация = models.CharField(max_length=255, blank=True)
    Подразделение = models.CharField(max_length=255, blank=True)
    Телефон = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)
