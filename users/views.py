from django.shortcuts import render,redirect
from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests as req
from .models import *
from django.contrib.auth import authenticate, login , logout
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET','POST'])
def login_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            if not user.check_password(password):
                return render(request,'error.html',context={'error':'Incorrect password'})
            login(request,user)

        except:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            red = redirect('/new_user/')
            red.set_cookie('user',username)
            return red 
        red = render(request,'home.html')
        red.set_cookie('user',username)
        return red
    return render(request,'login.html')

# @api_view(['GET','POST'])
@csrf_exempt
@login_required(login_url='/login/')
def new_user(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        phone = request.POST.get('phone')
        user = User.objects.get(username = request.COOKIES.get('user'))
        user.age = age
        user.weight = weight
        user.phone = phone
        user.save()
        return redirect('/home')
    return render(request,'new_user.html')

@csrf_exempt
@login_required(login_url='/login/')
def home(request):

    user = User.objects.get(username = request.COOKIES.get('user'))
    items_query = Items.objects.filter(user = user)
    total = 0
    for i in items_query:
        total += float(i.calorie)
    if request.method == 'POST':
        food = request.POST.get('food')
        try:
            results = req.get(f'https://www.myfitnesspal.com/api/nutrition?query={food}&page=1&offset=1')
            results = results.json()
            unit = results['items'][0]['item']['nutritional_contents']['energy']['unit']
            value = results['items'][0]['item']['nutritional_contents']['energy']['value']
            protein = results['items'][0]['item']['nutritional_contents']['protein']
        except:
            print('error')
            return render(request,'home.html',context = {'show':False })

        return render(request,'home.html',context = {'show':True,'unit':unit,'value':value,'protein':protein,'food':food ,'items':items_query , 'total':total})
    return render(request,'home.html',context={'items':items_query, 'total':total})

@csrf_exempt
@login_required(login_url='/login/')
def addfood(request):
    user = User.objects.get(username = request.COOKIES.get('user'))
    food_name = request.GET.get('food')
    value = request.GET.get('value')
    new_food = Items()
    new_food.user = user
    new_food.name = food_name
    new_food.calorie = value
    new_food.save()

    return redirect('/home')

@csrf_exempt
@login_required(login_url='/login/')
def removefood(request):
    user = User.objects.get(username = request.COOKIES.get('user'))
    food_id = request.GET.get('food')
    (Items.objects.get(id = food_id,user = user).delete())
    return redirect('/home')

@csrf_exempt
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return render(request,'login.html')

#TODO
#recipe
#all nutritional values
#passed day food 
#required food intake calories
#required nutrition
#logout
