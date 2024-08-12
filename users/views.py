from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import User, Follow
from django.http import JsonResponse

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

                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home')
                
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username').lower()
                password = login_form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home') 
                else:
                    login_form.add_error(None, 'Invalid username or password')

    return render(request, 'login.html', {'register_form': register_form, 'login_form': login_form})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        return JsonResponse({'status': 'same-account'})

    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    if not created:
        follow.delete()
        return JsonResponse({'status': 'unfollowed'})
    
    return JsonResponse({'status': 'followed'})


@login_required
def connect_wallet(request):
    return render(request, 'connect-wallet.html')