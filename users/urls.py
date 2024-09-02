from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', login_register_view, name='login'),
    path('<int:user_id>/follow/', follow_user, name='follow'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-code/', verify_code, name='verify_code'),
    path('reset-password/', reset_password, name='reset_password'),
    path('update/<str:username>', update_profile, name='update_profile'),
    path('logout/', logout_view, name='logout'),
]
