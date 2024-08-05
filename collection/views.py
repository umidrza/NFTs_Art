from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from users.models import User
from django.utils import timezone
from django.db.models import Case, When, Value, CharField
from django.contrib.auth.decorators import login_required

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

def collection_detail(request, id): 
    collection = get_object_or_404(Collection, id=id)
    currencies = Currency.objects.all()

    now = timezone.now()
    nfts = collection.nfts.annotate(
        status=Case(
            When(auction__isnull=False, auction__end_time__lt=now, then=Value('expired')),   
            When(auction__isnull=False, then=Value('auction')),
            default=Value('not-on-sale'),
            output_field=CharField(),
        )
    )
    
    context = {
        'collection': collection,
        'nfts': nfts,
        'currencies': currencies,
    }
    return render(request, 'collection-detail.html', context)


@login_required
def follow_creator(request, creator_id):
    creator = get_object_or_404(User, id=creator_id)
    request.user.following.add(creator)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def unfollow_creator(request, creator_id):
    creator = get_object_or_404(User, id=creator_id)
    request.user.following.remove(creator)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))