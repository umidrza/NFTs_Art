from django.urls import path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('', collections_list, name='list'),
]
