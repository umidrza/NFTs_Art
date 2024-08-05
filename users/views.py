from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm
from .models import User

def login_register_view(request):
    register_form = RegisterForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST, request.FILES)
            if register_form.is_valid():
                user = register_form.save()
                
                new_user = authenticate(username=user.username, password=request.POST['password1'])
                if new_user is not None:
                    login(request, new_user)
                    return redirect('home')
                
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username').lower()
                password = login_form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home') 
                else:
                    login_form.add_error(None, 'Invalid username or password')

    return render(request, 'login.html', {'register_form': register_form, 'login_form': login_form})
