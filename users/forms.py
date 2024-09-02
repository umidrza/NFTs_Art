from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Avatar

class RegisterForm(UserCreationForm):
    fullname = forms.CharField(max_length=30, required=True)
    avatar = forms.ModelChoiceField(queryset=Avatar.objects.all(), required=False, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'avatar', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class UpdateProfileForm(forms.ModelForm):
    fullname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    avatar = forms.ModelChoiceField(queryset=Avatar.objects.all(), required=False, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'avatar']
