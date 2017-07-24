from django.shortcuts import render, redirect
from .models import UserManager, User
from django.contrib import messages
# Create your views here.

def index(request):
    try:
        if request.session['logged'] != 0:
            return redirect('event:index')
        else:
            return render(request, 'login/index.html')
    except:
        return render(request, 'login/index.html')


def register(request):
    try:
        user_valid = User.objects.register(dict(request.POST.items()))
    except:
        request.session['logged']=0
        return redirect('/')
    if user_valid['register']:
        user = user_valid['user']
        messages.add_message(request, messages.INFO, 'Thanks ' + user.first_name  + ' For Creating An Account')
        return redirect('login:index')
    else:
        request.session['logged'] = 0
        for error in user_valid['error']:
            messages.add_message(request, messages.INFO, error)
        return redirect('login:index')


def login(request):
    try:
        user_valid = User.objects.login(dict(request.POST.items()))
    except:
        request.session['logged'] = 0
        return redirect('login:index')
    if user_valid['login']:
        user = user_valid['user']
        request.session['logged'] = user.id
        return redirect('belt:index')
    else:
        request.session['logged'] = 0
        for error in user_valid['error']:
            messages.add_message(request, messages.INFO, error)
        return redirect('login:index')

def logout(request):
    request.session['logged'] = 0
    request.session.flush()
    return redirect('login:index')
