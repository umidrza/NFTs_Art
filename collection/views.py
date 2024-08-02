from django.shortcuts import render
from .models import *

# Create your views here.
def collections_list(request):
    collections = Collection.objects.all()
    categories = Category.objects.all()
    blockchains = Blockchain.objects.all()

    context = {
        'collections': collections,
        'categories': categories,
        'blockchains': blockchains,
    }

    return render(request, 'collections.html', context)