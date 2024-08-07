from django.shortcuts import render, get_object_or_404
from .models import *
from users.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Follow


def collections_list(request):
    collections = Collection.objects.all()
    categories = Category.objects.all()
    blockchains = Blockchain.objects.all()
    following = User.objects.filter(followers__follower=request.user)

    context = {
        'collections': collections,
        'categories': categories,
        'blockchains': blockchains,
        'following': following,
    }

    return render(request, 'collections.html', context)

def collection_detail(request, id): 
    collection = get_object_or_404(Collection, id=id)
    currencies = Currency.objects.all()
    following = Follow.objects.filter(follower=request.user, following=collection.creator).exists()
    nfts = NFT.objects.prefetch_related('auctions').all()
    
    context = {
        'collection': collection,
        'nfts': nfts,
        'currencies': currencies,
        'following': following,
    }
    return render(request, 'collection-detail.html', context)


def nft_detail(request, collection_id, nft_id):
    collection = get_object_or_404(Collection, id=collection_id)
    nft = get_object_or_404(NFT, id=nft_id)
    liked = Like.objects.filter(nft=nft, user=request.user).exists()

    context = {
        'collection': collection,
        'nft': nft,
        'liked': liked,
    }
    return render(request, 'nft-detail.html', context)


@login_required
def like_nft(request, nft_id):
    nft = get_object_or_404(NFT, id=nft_id)
    like, created = Like.objects.get_or_create(nft=nft, user=request.user)
    
    if not created:
        like.delete()
        return JsonResponse({'status': 'unliked'})
    
    return JsonResponse({'status': 'liked'})