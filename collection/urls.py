from django.urls import path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('', collections_list, name='list'),
    path('<int:id>/detail/', collection_detail, name='detail'),
    path('follow/<int:creator_id>/', follow_creator, name='follow_creator'),
    path('unfollow/<int:creator_id>/', unfollow_creator, name='unfollow_creator'),
]
