from django.urls import path
from .views import connect_wallet

app_name = 'wallet'

urlpatterns = [
    path('', connect_wallet, name='connect'),
]