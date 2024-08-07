from django.urls import path
from .views import follow_user

app_name = 'user'

urlpatterns = [
    path('<int:user_id>/follow/', follow_user, name='follow'),
]
