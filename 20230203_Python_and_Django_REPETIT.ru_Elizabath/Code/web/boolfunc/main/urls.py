from django.urls import path
from .views import *

urlpatterns = [
    path('', BoolFunc.as_view(), name="home"),
    path('about-us', about, name='about'),
    path('create', create, name='create'),
    path('register', register_user, name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('profile/<int:pk>/', Account.as_view(), name='profile'),
    path('StartTask/Func', func, name='Func'),
    path('StartTask/Res', res, name='Res'),
    path('StartTask/FuncFromRes', funcFromRes, name='FuncFromRes'),
    path('StartTask/NameFunc', nameFunc, name='NameFunc'),
    path('StartTask/FictVar', fictVar, name='FictVar'),
    path('StartTask/DNF', dnf, name='DNF'),
    path('StartTask/KNF', knf, name='KNF'),
    path('StartTask/SDNF', sdnf, name='SDNF'),
    path('StartTask/SKNF', sknf, name='SKNF'),
]