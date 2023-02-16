from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    group = models.CharField('Группа', max_length=20)
    rating = models.IntegerField('Рейтинг', max_length=20, default=0)
    kontrol_task1 = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Task(models.Model):
    title = models.CharField('Название', max_length=255)
    task = models.TextField('Описание')
    type = models.CharField('Тип задачи', max_length=50, default="none")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'