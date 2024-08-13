from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', login_register_view, name='login'),
    path('<int:user_id>/follow/', follow_user, name='follow'),
]
