from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime, timedelta
import pytz

def index(request):
    return render(request, 'login_app/index.html')

def success(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            return render(request, 'login_app/wall.html')
        else:
            return redirect('/')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()) 
            new_user= User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = new_user.id 
            request.session['first_name'] = new_user.first_name
            return redirect('/wall')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/wall')
        else:
            messages.error(request, 'Account not found. Register now!')
            return redirect('/')


def logout(request):
    if request.method == 'GET':
        request.session.clear()
    return redirect('/')

def wall(request):
    context = {
        'posts': Message.objects.all().order_by('-created_at')
    }
    
    return render(request, 'login_app/wall.html', context)

def post_message(request):
    if request.method == 'POST':
        Message.objects.create(
            message=request.POST['post_message'],
            user = User.objects.get(id=request.session['user_id']))
    return redirect('/wall')

def post_comment(request, message_id):
    if request.method == 'POST':
        Comment.objects.create(
            message=Message.objects.get(id= message_id),
            user=User.objects.get(id=request.session['user_id']),
            comment=request.POST['post_comment']
        )
    return redirect('/wall')

def delete(request, message_id):
    message = Message.objects.get(id= message_id)
    if request.session['user_id'] == message.user.id:
        print(message.created_at.tzinfo)
        print(datetime.utcnow().tzinfo)
        # message.created_at is aware, datetime.utcnow() is naive
        if message.created_at > pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=30):
            message.delete()
            return redirect('/wall')
        else:
            messages.error(request, 'Oops. You can only delete your own messages if they were posted in the last 30 minutes.')
            return redirect('/wall') 
    
    