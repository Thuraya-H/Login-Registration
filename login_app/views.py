from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib import messages

def index(request):
    return render(request,'login.html')

def register(request): 
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name_f=request.POST['first_name']
        last_name_f=request.POST['last_name']
        bday_f=request.POST['bday']
        email_f=request.POST['email']
         
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        print(pw_hash)
        
        reg_user = User.objects.create(first_name=first_name_f, last_name=last_name_f, birthday=bday_f,email=email_f, password=pw_hash) 
        messages.success(request, "User successfully created")
        request.session['userid'] = reg_user.id
        request.session['enter_message'] = "registered"
        return redirect('/success') 

def log(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            request.session['enter_message'] = "logged in"
            return redirect('/success')
        else:
            messages.error(request,'Incorrect password entered!')
            return redirect('/')
    else:
        messages.error(request,'incorrect Email Address or Password!')
        return redirect('/')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id = request.session['userid'])
        }
        return render(request,'success.html',context)

def destroy(request):
    del request.session['userid']
    del request.session['enter_message']
    return redirect('/')