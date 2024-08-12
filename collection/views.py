from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from users.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Follow
from wallet.models import Wallet
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse


def collections_list(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        collections = Collection.objects.filter(creator=user)
        title = 'My Collections' if user == request.user else f"{user.fullname}'s Collections"
    else:
        collections = Collection.objects.all()
        title = 'Get Popular Collection'
    
    categories = Category.objects.all()
    blockchains = Blockchain.objects.all()
    following = User.objects.filter(followers__follower=request.user) if request.user.is_authenticated else User.objects.none()

    context = {
        'collections': collections,
        'categories': categories,
        'blockchains': blockchains,
        'following': following,
        'title': title,
    }

    return render(request, 'collections.html', context)


def collection_detail(request, id): 
    collection = get_object_or_404(Collection, id=id)
    creator = collection.creator
    currencies = Currency.objects.all()
    following = Follow.objects.filter(follower=request.user, following=creator).exists() if request.user.is_authenticated else False
    nfts = collection.nfts.prefetch_related('auctions').all()
    
    context = {
        'collection': collection,
        'nfts': nfts,
        'creator': creator,
        'currencies': currencies,
        'following': following,
    }
    return render(request, 'collection-detail.html', context)


@login_required
def collection_create_update(request, collection_id=None):
    blockchains = Blockchain.objects.all()
    categories = Category.objects.all()
    collection = get_object_or_404(Collection, id=collection_id, creator=request.user) if collection_id else None
    
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user
            collection.save()

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('collection:user_collections', request.user.username)
    else:
        form = CollectionForm(instance=collection)

    context = {
        'form': form,
        'blockchains': blockchains,
        'categories': categories,
        'is_update': collection_id is not None,
        'collection': collection,
    }

    return render(request, 'collection-create.html', context)


@login_required
def collection_delete(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    collection.delete()
    return redirect('collection:user_collections', request.user.username)


def nft_detail(request, nft_id, collection_id=None, auction_id = None):
    nft = get_object_or_404(NFT, id=nft_id)
    collection = get_object_or_404(Collection, id=collection_id) if collection_id else nft.collections.first()
    collection_nfts = collection.nfts.exclude(id=nft.id)[:4] if collection else None
    auction = get_object_or_404(Auction, id=auction_id) if auction_id else nft.auctions.first()
    liked = Like.objects.filter(nft=nft, user=request.user).exists() if request.user.is_authenticated else False
    status = nft.get_status(auction)

    context = {
        'nft': nft,
        'collection': collection,
        'collection_nfts': collection_nfts,
        'auction': auction,
        'status': status,
        'liked': liked,
    }
    return render(request, 'nft-detail.html', context)


@login_required
def user_nfts(request, username):
    creator = get_object_or_404(User, username=username)
    nfts = NFT.objects.filter(creator=creator)
    currencies = Currency.objects.all()

    context = {
        'nfts': nfts,
        'creator': creator,
        'currencies': currencies,
    }

    return render(request, 'collection-detail.html', context)


@login_required
def nft_create(request):
    collections = Collection.objects.filter(creator=request.user)
    blockchains = Blockchain.objects.all()
    if request.method == 'POST':
        form = NFTForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            nft = form.save(commit=False)
            nft.creator = request.user
            nft.save()
            form.save_m2m()
            return redirect('collection:nft_detail', nft_id=nft.id)
    else:
        form = NFTForm(user=request.user)

    context = {
        'form': form,
        'blockchains': blockchains,
        'collections': collections,
    }
    
    return render(request, 'nft-create.html', context)


@login_required
def nft_sell(request, nft_id, auction_id=None):
    currencies = Currency.objects.all()
    nft = get_object_or_404(NFT, id=nft_id)
    auction = get_object_or_404(Auction, id=auction_id) if auction_id else None
    wallet_id = request.GET.get('wallet_id')
    wallet = get_object_or_404(Wallet, id=wallet_id) if wallet_id else None

    if request.method == 'POST':
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.nft = nft
            auction.saler = request.user
            auction.save()
            return redirect('collection:auction_sell', nft.id, auction.id)
    else:
        form = AuctionForm(instance=auction)

    context = {
        'form': form,
        'currencies': currencies,
        'nft': nft,
        'auction': auction,
        'wallet': wallet,
    }

    return render(request, 'nft-sell.html', context)


@login_required
def auction_update(request, auction_id):
    currencies = Currency.objects.all()
    auction = get_object_or_404(Auction, id=auction_id)
    nft = auction.nft

    if request.method == 'POST':
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            auction = form.save()
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('collection:auction_detail', auction.nft.id, auction.id)
    else:
        form = AuctionForm(instance=auction)

    context = {
        'form': form,
        'currencies': currencies,
        'nft': nft,
        'auction': auction,
        'update': True,
    }

    return render(request, 'nft-sell.html', context)

@login_required
def auction_delete(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    auction.delete()
    return redirect('collection:user_nfts', request.user.username)


@login_required
def nft_like(request, nft_id):
    nft = get_object_or_404(NFT, id=nft_id)
    like, created = Like.objects.get_or_create(nft=nft, user=request.user)
    
    if not created:
        like.delete()
        return JsonResponse({'status': 'unliked'})
    
    return JsonResponse({'status': 'liked'})