from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        now = datetime.now()
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email = postData['email'])) != 0:
            errors['email_unique'] = "That email address is already in use"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Your first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Your last name should be at least 2 characters"
        if datetime.strptime(postData['birthday'], "%m/%d/%Y") > now:
            errors['birthday'] = 'Your birthday must be in the past'
        if len(postData['password']) < 8:
            errors["password"] = "Your password must be at least 8 characters"
        if postData['confirm_pw'] != postData['password']:
            errors["confirm_pw"] = "Your passwords must match"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField(null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
