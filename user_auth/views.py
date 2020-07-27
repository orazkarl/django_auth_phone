from django.shortcuts import render, HttpResponse
from django.views import generic
from .forms import UserCreateForm, UserAuthForm, UserResetPassoword
from .models import User
from django.contrib.auth import login, logout, authenticate
import random
import requests

MOBIZON_API_KEY = 'kz79254c7b79ab00e882f92418131e194df3783a54052356ff64a2623c9f40a19e8ca6'
DOMEN_API = 'api.mobizon.kz'


def sign_up(request):
    if request.POST:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = str(random.randrange(1000, 9999))

            print(password)
            url = 'https://api.mobizon.kz/service/message/sendsmsmessage?' \
                  'recipient=' + str(phone).split('+')[1] + '&' \
                                                            'text=Vash+parol+dlya+vhoda:+' + password + \
                  '&apiKey=' + MOBIZON_API_KEY
            requests.get(url=url)
            username = str(phone).split('+')[1]
            is_used = False
            try:
                is_used = User.objects.get(phone=phone)
            except Exception as e:
                print(e)
            user = None
            if not is_used:
                user = User.objects.create_user(username=username, phone=phone, password=password)
            else:
                return HttpResponse('Номер занят')

            try:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('success')
                else:
                    return HttpResponse('Пользователь заблокирован')
            except Exception:
                return HttpResponse('Пользователь не найден')
        else:
            return HttpResponse('Пользователь с таким номером уже существует')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


def sign_in(request):
    if request.POST:
        form = UserAuthForm(request.POST)
        print(form)
        if form.is_valid():
            phone = request.POST['phone']
            password = request.POST['password']
            username = str(phone).split('+')[1]
            print(username, password)
            try:
                user = authenticate(username=username, password=password)
                if user.is_active:
                    login(request, user)
                    return HttpResponse('success')
                else:
                    return HttpResponse('Пользователь заблокирован')
            except Exception as e:
                user = None
                return HttpResponse('Неверно введены данные')
    else:
        form = UserAuthForm()
    return render(request, 'registration/login.html', {'form': form})


def reset_password(request):
    if request.method == 'POST':
        form = UserResetPassoword(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = str(random.randrange(1000, 9999))
            print(password)
            url = 'https://api.mobizon.kz/service/message/sendsmsmessage?' \
                  'recipient=' + str(phone).split('+')[1] + '&' \
                                                            'text=Vash+parol+dlya+vhoda:+' + password + \
                  '&apiKey=' + MOBIZON_API_KEY
            requests.get(url=url)
            username = str(phone).split('+')[1]
            try:
                user = User.objects.create_user(username=username, phone=phone, password=password)
            except Exception:
                return HttpResponse('Пользователь не найден')
            try:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('success')
                else:
                    return HttpResponse('Пользователь заблокирован')
            except Exception:
                return HttpResponse('Пользователь не найден')

    else:
        form = UserResetPassoword()
    return render(request, 'registration/signup.html', {'form': form})
