from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *
from django.forms import ModelForm, TextInput, Textarea, PasswordInput, CharField, EmailField, EmailInput


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            })
        }


class RegisterUserForm(UserCreationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    first_name = CharField(label='Имя', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = CharField(label='Фамилия', widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(label='Email', widget=EmailInput(attrs={'class': 'form-control'}))
    password1 = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(label='Повтор пароля', widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['group']
        labels = {
            'group': 'Группа'
        }
        widgets = {
            "group": TextInput(attrs={
                'class': 'form-control'
            })
        }


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'password')

