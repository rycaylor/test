# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login.models import User
from django.contrib import messages
from .models import Cat, Like

# Create your views here.
def index(request):
    if 'logged' not in request.session:
        return redirect('login:index')
    else:
        try:
            context = {
                    'user': User.objects.get(id=int(request.session['logged'])),
                    'cats' : Cat.objects.all(),
                    'like' : Like.objects.all(),
                }
            return render(request, 'belt_test/index.html', context)
        except:
            return redirect('login:index')

def add(request):
    if 'logged' not in request.session:
        return redirect('login:index')
    else:
        return render(request, 'belt_test/add.html')


def make_cat(request):
    user = int(request.session['logged'])
    cat_valid = Cat.objects.make_cat(dict(request.POST.items()), user)
    if cat_valid['create']:
        cat = cat_valid['cat']
        user = User.objects.get(id=user)
        messages.add_message(request, messages.INFO, 'Thanks ' + user.first_name  + ' For adding, ' + cat.name + '!')
        return redirect('belt:add')
    else:
        for error in cat_valid['error']:
            messages.add_message(request, messages.INFO, error)
            return redirect('belt:add')


def info(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    cat = int(id)
    context = {
        'cat': Cat.objects.get(id=cat)
    }
    return render(request, 'belt_test/info.html', context)



def edit(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    cat = int(id)
    context = {
        'cat': Cat.objects.get(id=cat)
    }
    return render(request, 'belt_test/edit.html', context)



def change(request):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    cat_change = Cat.objects.make_change(dict(request.POST.items()), user)
    if cat_change['create']:
        cat = cat_change['cat']
        user = User.objects.get(id=user)
        messages.add_message(request, messages.INFO, 'Thanks ' + user.first_name  + ' For changing, ' + cat.name + '!')
        return redirect('belt:index')
    else:
        for error in cat_valid['error']:
            messages.add_message(request, messages.INFO, error)
            return redirect('belt:edit')

def like(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    cat = int(id)
    like_inc = Like.objects.make_like(user, cat)
    return redirect('belt:index')


def unlike(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    cat = int(id)
    unlike_rev = Like.objects.make_unlike(user, cat)
    return redirect('belt:index')

def delete(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    cat = int(id)
    make_delete = Cat.objects.make_delete(user, cat)
    return redirect('belt:index')
