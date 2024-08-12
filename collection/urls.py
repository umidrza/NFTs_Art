from django.urls import path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('', collections_list, name='list'),
    path('<int:id>/', collection_detail, name='detail'),
    path('create/', collection_create_update, name='create'),
    path('<int:collection_id>/update/', collection_create_update, name='update'),
    path('<int:collection_id>/delete/', collection_delete, name='delete'),
    path('nft/create/', nft_create, name='nft_create'),
    path('<int:collection_id>/nft/<int:nft_id>/', nft_detail, name='collection_nft_detail'),
    path('nft/<int:nft_id>/', nft_detail, name='nft_detail'),
    path('nft/<int:nft_id>/auction/<int:auction_id>/', nft_detail, name='auction_detail'),
    path('nft/<int:nft_id>/sell/', nft_sell, name='nft_sell'),
    path('nft/<int:nft_id>/auction/<int:auction_id>/sell/', nft_sell, name='auction_sell'),
    path('auction/<int:auction_id>/update', auction_update, name='auction_update'),
    path('auction/<int:auction_id>/delete', auction_delete, name='auction_delete'),
    path('nft/<int:nft_id>/like/', nft_like, name='nft_like'),
    path('<str:username>/', collections_list, name='user_collections'),
    path('<str:username>/nfts/', user_nfts, name='user_nfts'),
]
