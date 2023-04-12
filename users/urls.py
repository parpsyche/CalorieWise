from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("login/", login_register,name='login/register'),
    path("new_user/", new_user,name='new_user'),
    path("home/", home,name='home'),
    path("addfood/", addfood,name='addfood'),
    path("removefood/", removefood,name='removefood'),
    path("logout/", logout_user,name='logout'),
]
