# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User
# Create your models here.

class CatManager(models.Manager):
    def make_cat(self, postData, user):
        results = {'create':True, 'error':[], 'cat':None}
        if postData['name'] == '':
            results['create']=False
            results['error'].append('Please enter a name for your awesome cat!')
        else:
            name = postData['name']
        if postData['age'] == '':
            results['create'] = False
            results['error'].append('Please enter an age for your awesome cat!')
        elif type(int(postData['age'])) != int:
            results['create'] = False
            results['error'].append('Please enter an integer for your cats age :)')
        else:
            age = int(postData['age'])

        if results['create']:
            cat = Cat.objects.create(name = name, age = age, user_id = user)

            cat.save()
            results['cat'] = cat

        return results

    def make_delete(self, user, cat):
        delete_it = Cat.objects.filter(user_id=user).filter(id=cat).delete()
        return delete_it


    def make_change(self, postData, user):
        results = {'create':True, 'error':[], 'cat':None}
        cat = int(postData['cat'])
        if postData['name'] == '':
            results['create']=False
            results['error'].append('Please enter a name for your awesome cat!')
        else:
            name = postData['name']
        if postData['age'] == '':
            results['create'] = False
            results['error'].append('Please enter an age for your awesome cat!')
        elif type(int(postData['age'])) != int:
            results['create'] = False
            results['error'].append('Please enter an integer for your cats age :)')
        else:
            age = int(postData['age'])

        if results['create']:
            old_cat = Cat.objects.get(id=cat)
            old_cat.name = name
            old_cat.age = age

            old_cat.save()

            results['cat']=old_cat

        return results



class LikeManager(models.Manager):
    def make_like(self, user, cat):
        if len(Like.objects.filter(user_id=user).filter(cat_id=cat)) >0:
            print Like.objects.filter(user_id=user).filter(cat_id=cat)
            print 'no'
            return None
        else:
            like = Like.objects.create(user_id = user, cat_id = cat)
            print 'yes'
            return like

    def make_unlike(self, user, cat):
        unlike = Like.objects.filter(user_id=user).filter(cat_id=cat).delete()
        return unlike






class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    user = models.ForeignKey(User, related_name='user_cat')
    def get_like_users(self):
        likes = Like.objects.filter(cat_id=self.id)

        user = []
        for like in likes:
            user.append(like.user_id)
        return user
    objects = CatManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    cat = models.ForeignKey(Cat, related_name = 'cat_like')
    user = models.ForeignKey(User, related_name='user_like')
    objects = LikeManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
