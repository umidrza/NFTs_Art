from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import User, Follow
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
import random
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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
                    messages.success(request, 'Registration successful. You are now logged in.')

                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'There was an issue logging in after registration. Please try logging in manually.')
                
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username').lower()
                password = login_form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back {user.fullname}')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home') 
                else:
                    login_form.add_error(None, 'Invalid username or password')

    context = {
        'register_form': register_form, 
        'login_form': login_form
    }

    return render(request, 'login.html', context)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        return JsonResponse({'status': 'same-account'})

    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    if not created:
        follow.delete()
        follower_count = user_to_follow.followers.count()
        return JsonResponse({'status': 'unfollowed', 'follower_count': follower_count})
    
    follower_count = user_to_follow.followers.count()
    return JsonResponse({'status': 'followed' , 'follower_count': follower_count})
    

def forgot_password(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        token = str(random.randint(100000, 999999))
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        send_mail(
            'Password Reset Verification Code',
            f'Your verification code is: {token}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        request.session['uid'] = uid
        request.session['token'] = token
        return JsonResponse({'message': 'Verification code has been sent to your email.', 'success': True})
    else:
        return JsonResponse({'message': 'No account found with this email.', 'success': False})


def verify_code(request):
    submitted_token = request.POST.get('token')
    stored_token = request.session.get('token')
    uid = request.session.get('uid')
    if uid is None or stored_token is None:
        return JsonResponse({'message': 'Session expired. Please try again.', 'success': False})

    if submitted_token == stored_token:
        request.session.pop('token')
        return JsonResponse({'message': 'Code verified. Proceed to reset password.', 'success': True})
    else:
        return JsonResponse({'message': 'Invalid verification code.', 'success': False})


def reset_password(request):
    new_password = request.POST.get('password')
    uid = request.session.get('uid')

    if uid is None:
        return JsonResponse({'message': 'Session expired. Please try again.', 'success': False})
    
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return JsonResponse({'message': e.messages[:1], 'success': False})

        user.set_password(new_password) 
        user.save()

        return JsonResponse({'message': 'Password has been reset successfully.', 'success': True})
    except User.DoesNotExist:
        return JsonResponse({'message': 'Invalid session. Please try again.', 'success': False})
