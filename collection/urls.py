from django.urls import path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('', collections_list, name='list'),
    path('<int:id>/', collection_detail, name='detail'),
    path('<int:collection_id>/nft/<int:nft_id>/', nft_detail, name='nft_detail'),
    path('<int:nft_id>/like/', like_nft, name='like_nft'),
]
