from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', home_view, name='index'),
    path('roadmap/', roadmap_view, name='roadmap'),
    path('ourclans/', ourclans_view, name='ourclans'),
    path('faq/', faq_view, name='faq'),
]
