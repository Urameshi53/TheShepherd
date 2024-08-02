from datetime import timezone
from typing import Any, Dict
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from django.views import generic
from django.template import RequestContext
import re

from .forms import LoginForm, RegistrationForm, ResetPasswordForm
from discussions.models import Student

other_error_messages = []

class ProfileView(generic.DetailView):
    template_name = "accounts/profile.html"
    model = Student 

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['student'] = Student.objects.filter(user=self.request.user)[0]

        return context

def login(request):
    error_messages = []
    context = {}
    form = LoginForm
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #user = authenticate(request, email=email, password=password)
        user = None
        for i in User.objects.all():
            if i.email == email and i.check_password(password):
                user = i
                
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('admin')
            else:
                return redirect('home')
        else: 
            error_messages.append('Email or password is not correct')
            messages.error(request, 'Username or password does not match')
            print('did not work')
    else:
        pass    

    return render(request, 'accounts/login.html', {'form':form, 'error_messages':error_messages})#, RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('home')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if (re.fullmatch(regex, email)):
        return True 
    else:
        return False

def signup_view(request):
    error_messages = []
    form = RegistrationForm
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        location = request.POST.get('location')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2 and check_email(email):
            '''html_message = render_to_string('accounts/email_message.html')
            message = 'Thank you'
            send_mail(f'Hello {username}, thank you for registering with MicroFocus.', message, 'zigahemmanuel53@gmail.com', ['emmanuelzigah2019@gmail.com',], html_message=html_message)
                      '''  
            user = User()
            user.username = username
            user.email = email
            user.set_password(password1)
            user.save()

            auth_login(request, user)
            #return render(request, 'accounts/send_email.html')
            return redirect('home')
        else:
            if password1 != password2:
                error_messages.append('Passwords do not match')
            else:
                error_messages.append('Incorrect email')                
    else:
        pass    

    return render(request, 'accounts/signup.html', {'form':form, 'error_messages':error_messages})


def reset_view(request, user_id):
    form = ResetPasswordForm
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.get(id=user_id)

        if user.check_password(old_password) and password1 == password2:
            user.set_password(password1)
            user.save()    
            #auth_login(request, user)
            return redirect('home')
        else:
            auth_login(request, user)
            if password1 != password2:
                other_error_messages.append('passwords did not match')
            else:
                other_error_messages.append('Old password is wrong')
            return HttpResponseRedirect(f"/accounts/{user_id}/")

