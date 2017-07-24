from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z][0-9a-zA-Z .,-]*$')
class UserManager(models.Manager):

    def register(self, postData):
        results = {'register': True, 'error': [], 'user': None}
        if postData['first'] == '':
            results['register'] = False
            results['error'].append('Required First Name')
        elif not NAME_REGEX.match(postData['first']):
            resutls['register'] = False
            results['error'].append('Not a Valid First Name')
        else:
            first_name = postData['first']
        if postData['last'] == '':
            results['register'] = False
            results['error'].append('Required Last Name')
        elif not NAME_REGEX.match(postData['last']):
            results['register'] = False
            results['error'].append('Not a Valid Last Name')
        else:
            last_name = postData['last']
        if not EMAIL_REGEX.match(postData['email']):
            results['register'] = False
            results['error'].append('Incorrect Email')
        try:
            User.objects.get(email=postData['email'])
            results['register'] = False
            results['error'].append('Email Already Exists')
        except:
            email = postData['email']
        if len(postData['pass1']) < 8:
            results['results'] = False
            results['error'].append('Password must be at least 8 characters')
        elif postData['pass1'] != postData['pass2']:
            results['register'] = False
            results['error'].append('passwords do not match')

        elif results['register']:
            HashPass = postData['pass1']
            HashPass = HashPass.encode()

            hashedpass = bcrypt.hashpw(HashPass, bcrypt.gensalt())

            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashedpass)

            user.save()
            results['user']=user
        return results

    def login(self, postData):
        results = {'login':True, 'error': [], 'user':None}
        emailTest = postData['emailTest']
        try:
            user = User.objects.get(email=emailTest)
            password = postData['passTest']
            password = password.encode()
            test = user.password.encode()
            password = bcrypt.hashpw(password, test)
            if password == user.password:
                results['register'] = True
                results['user']=user
                return results
            else:
                results['login'] = False
                results['error'].append('Incorrect Email/Password Combination')
                return results
        except:
            results['login'] = False
            results['error'].append('Incorrect Email/Password Combination')
            return results


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
