from django.urls import path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('', collections_list, name='list'),
    path('<int:id>/', collection_detail, name='detail'),
    path('<int:collection_id>/nft/<int:nft_id>/', collection_nft_detail, name='collection_nft_detail'),
    path('nft/<int:nft_id>/', nft_detail, name='nft_detail'),
    path('nft/create/', nft_create, name='nft_create'),
    path('nft/<int:nft_id>/sell/', nft_sell, name='nft_sell'),
    path('nft/<int:nft_id>/like/', nft_like, name='nft_like'),
]
