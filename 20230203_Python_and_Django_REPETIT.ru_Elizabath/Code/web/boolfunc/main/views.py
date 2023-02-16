from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .practice import *
from django.views.generic import ListView, CreateView, DetailView

# def index(request):
#     tasks = Task.objects.all()
#     profile = Profile
#     return render(request, 'main/index.html', {'tasks': tasks, 'profile': profile, 'title': 'Главная страница'})


class BoolFunc(ListView):
    model = Task
    template_name = 'main/index.html'
    context_object_name = 'tasks'
    extra_context = {'title': 'Главная страница'}


def about(request):
    return render(request, 'main/about.html')


def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма неверна'

    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)


def func(request):
    task = Task.objects.get(type="Func")
    fn = BFuncion.random(4)
    print(fn)
    return render(request, 'main/starttask/Func.html', {'task': task, 'Bfunc': fn})


def res(request):
    task = Task.objects.get(type="Res")
    return render(request, 'main/starttask/Res.html', {'task': task})


def funcFromRes(request):
    task = Task.objects.get(type="FuncFromRes")
    return render(request, 'main/starttask/FuncFromRes.html', {'task': task})


def nameFunc(request):
    task = Task.objects.get(type="NameFunc")
    return render(request, 'main/starttask/NameFunc.html', {'task': task})


def fictVar(request):
    task = Task.objects.get(type="FictVar")
    return render(request, 'main/starttask/FictVar.html', {'task': task})


def dnf(request):
    task = Task.objects.get(type="DNF")
    return render(request, 'main/starttask/DNF.html', {'task': task})


def knf(request):
    task = Task.objects.get(type="KNF")
    return render(request, 'main/starttask/KNF.html', {'task': task})


def sdnf(request):
    task = Task.objects.get(type="SDNF")
    return render(request, 'main/starttask/SDNF.html', {'task': task})


def sknf(request):
    task = Task.objects.get(type="SKNF")
    return render(request, 'main/starttask/SKNF.html', {'task': task})


def register_user(request):
    error = ''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('home')
        else:
            error = 'Форма неверна'

    form = RegisterUserForm()
    profile_form = ProfileForm()
    context = {
        'profile_form': profile_form,
        'form': form,
        'error': error
    }
    return render(request, 'main/register.html', context)


# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     profile_form = ProfileForm
#     template_name = 'main/register.html'
#     success_url = reverse_lazy('home')
#     extra_context = {'title': 'Регистрация'}


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    extra_context = {'title': 'Вход'}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class Account(DetailView):
    model = Profile
    template_name = 'main/account.html'
    extra_context = {'title': 'Личный кабинет'}

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(Account, self).get_context_data(*args, **kwargs)
        param = self.kwargs['pk']
        print(param)
        # page_user = get_object_or_404(Profile, user_id=param)
        # context['page_user'] = page_user
        return context
