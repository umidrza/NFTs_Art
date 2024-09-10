from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import *
from .models import *
from users.models import User, Follow
from wallet.models import Wallet, Blockchain
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Sum


def collections_list(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        collections = Collection.objects.filter(creator=user)
        title = 'My Collections' if user == request.user else f"{user.fullname}'s Collections"
    else:
        collections = Collection.objects.all()
        title = 'Get Popular Collection'

    top_collectors = User.objects.annotate(
        total_auction_price=Sum('nfts__auctions__price')
    ).order_by('-total_auction_price')[:12]
    half_count = len(top_collectors) // 2
    if half_count > 4:
        top_collectors_1 = top_collectors[:half_count]
        top_collectors_2 = top_collectors[half_count:]
    else:
        top_collectors_1 = top_collectors
        top_collectors_2 = []
    
    categories = Category.objects.all()
    blockchains = Blockchain.objects.all()
    following = User.objects.filter(followers__follower=request.user) if request.user.is_authenticated else User.objects.none()

    search_query = request.GET.get('search', '')
    blockchain_filter = request.GET.get('blockchain', 'all')
    category_filter = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by', 'default')

    if search_query:
        collections = collections.filter(name__icontains=search_query)

    if blockchain_filter != 'all' and blockchain_filter.isdigit():
        collections = collections.filter(blockchain__id=blockchain_filter)

    if category_filter:
        collections = collections.filter(category__id__in=category_filter)

    if sort_by == 'name-asc':
        collections = collections.order_by('name')
    elif sort_by == 'name-desc':
        collections = collections.order_by('-name')


    paginator = Paginator(collections, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {
            'page_obj': page_obj,
            'following': following,
            'request': request
        }
        html = render_to_string('partials/collection-cards.html', context)
        return JsonResponse({'html': html})
   
    context = {
        'categories': categories,
        'blockchains': blockchains,
        'following': following,
        'title': title,
        'page_obj': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'blockchain_filter': blockchain_filter,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'top_collectors_1': top_collectors_1,
        'top_collectors_2': top_collectors_2,
    }

    return render(request, 'collections.html', context)


def collection_detail(request, id=None, username=None): 
    if id:
        collection = get_object_or_404(Collection, id=id)
        collector = collection.creator
        nfts = collection.nfts.prefetch_related('auctions').all()
    elif username:
        collector = get_object_or_404(User, username=username)
        nfts = NFT.objects.filter(collectors=collector)
        collection = None

    top_collectors = User.objects.annotate(
        total_auction_price=Sum('nfts__auctions__price')
    ).order_by('-total_auction_price')[:12]
    half_count = len(top_collectors) // 2
    if half_count > 4:
        top_collectors_1 = top_collectors[:half_count]
        top_collectors_2 = top_collectors[half_count:]
    else:
        top_collectors_1 = top_collectors
        top_collectors_2 = []
    
    currencies = Currency.objects.all()
    following = Follow.objects.filter(follower=request.user, following=collector).exists() if request.user.is_authenticated else False
    
    status_filters = request.GET.getlist('status')
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')
    currency_filter = request.GET.get('currency', 'all')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'default')

    if min_value or max_value or currency_filter != 'all':
        nfts = nfts.filter(auctions__isnull=False)
        if min_value:
            nfts = nfts.filter(auctions__price__gte=min_value)
        if max_value:
            nfts = nfts.filter(auctions__price__lte=max_value)
        if currency_filter != 'all':
            nfts = nfts.filter(auctions__currency__symbol=currency_filter)

    if search_query:
        nfts = nfts.filter(name__icontains=search_query)
    
    if sort_by == 'price-asc':
        nfts = nfts.filter(auctions__isnull=False).order_by('auctions__price')
    elif sort_by == 'price-desc':
        nfts = nfts.filter(auctions__isnull=False).order_by('-auctions__price')
    elif sort_by == 'name-asc':
        nfts = nfts.order_by('name')
    elif sort_by == 'name-desc':
        nfts = nfts.order_by('-name')

    if status_filters:
        nfts = [nft for nft in nfts if nft.get_status() in status_filters]

    paginator = Paginator(nfts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {
            'page_obj': page_obj,
            'collection': collection,
        }
        html = render_to_string('partials/nft-cards.html', context)
        return JsonResponse({'html': html})
    
    context = {
        'collection': collection,
        'collector': collector,
        'currencies': currencies,
        'following': following,
        'page_obj': page_obj,
        'paginator': paginator,
        'status_filters': status_filters,
        'min_value': min_value,
        'max_value': max_value,
        'currency_filter': currency_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'top_collectors_1': top_collectors_1,
        'top_collectors_2': top_collectors_2,
    }
    return render(request, 'collection-detail.html', context)


@login_required
def collection_create_update(request, collection_id=None):
    blockchains = Blockchain.objects.all()
    categories = Category.objects.all()
    collection = get_object_or_404(Collection, id=collection_id, creator=request.user) if collection_id else None
    nfts = NFT.objects.filter(collectors=request.user)
    
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection, user=request.user)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user
            collection.save()
            form.save_m2m()

            if collection_id:
                messages.success(request, 'Collection updated successfully.')
            else:
                messages.success(request, 'Collection created successfully.')

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('collection:user_collections', request.user.username)
    else:
        form = CollectionForm(instance=collection, user=request.user)

    context = {
        'form': form,
        'blockchains': blockchains,
        'categories': categories,
        'is_update': collection_id is not None,
        'collection': collection,
        'nfts': nfts,
    }

    return render(request, 'collection-create.html', context)


@login_required
def collection_delete(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    collection.delete()
    messages.success(request, 'Collection deleted successfully.')
    return redirect('collection:user_collections', request.user.username)


def nft_detail(request, nft_id, collection_id=None, auction_id = None):
    nft = get_object_or_404(NFT, id=nft_id)
    collection = get_object_or_404(Collection, id=collection_id) if collection_id else nft.collections.first()
    collection_nfts = collection.nfts.exclude(id=nft.id)[:4] if collection else None
    auction = get_object_or_404(Auction, id=auction_id) if auction_id else nft.auctions.first()
    liked = Like.objects.filter(nft=nft, user=request.user).exists() if request.user.is_authenticated else False
    status = nft.get_status(auction)
    bids = Bid.objects.filter(auction=auction).order_by('timestamp') if auction else None
    bid_amounts = [float(bid.amount) for bid in bids] if bids else []
    bid_timestamps = [bid.timestamp.isoformat() for bid in bids] if bids else []
    
    context = {
        'nft': nft,
        'collection': collection,
        'collection_nfts': collection_nfts,
        'auction': auction,
        'status': status,
        'liked': liked,
        'bids': bids,
        'bid_amounts': bid_amounts,
        'bid_timestamps': bid_timestamps,
    }
    return render(request, 'nft-detail.html', context)


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
            nft.collectors.add(request.user)
            nft.collections.set(form.cleaned_data.get('collections'))
            form.save_m2m()
            messages.success(request, 'NFT created successfully.')
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
def auction_create(request, nft_id):
    currencies = Currency.objects.all()
    nft = get_object_or_404(NFT, id=nft_id)

    auction = Auction.objects.filter(saler=request.user, nft=nft).first()
    if auction: 
        messages.error(request, f"You have already submitted this form")
        return redirect('collection:auction_sell', auction.id)

    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.nft = nft
            auction.saler = request.user
            auction.save()
            return redirect('collection:auction_sell', auction.id)
    else:
        form = AuctionForm()

    context = {
        'form': form,
        'currencies': currencies,
        'nft': nft,
        'operation': 'create',
    }

    return render(request, 'nft-sell.html', context)


@login_required
def auction_sell(request, auction_id):
    currencies = Currency.objects.all()
    auction = get_object_or_404(Auction, id=auction_id)
    nft = auction.nft
    wallet_id = request.GET.get('wallet_id')
    wallet = get_object_or_404(Wallet, id=wallet_id) if wallet_id else None

    context = {
        'currencies': currencies,
        'nft': nft,
        'auction': auction,
        'wallet': wallet,
        'operation': 'sell',
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
            messages.success(request, 'Auction updated successfully.')
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
        'operation': 'update',
    }

    return render(request, 'nft-sell.html', context)


@login_required
def auction_delete(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    auction.delete()
    messages.success(request, 'Auction deleted successfully.')
    return redirect('collection:user_nfts', request.user.username)


@login_required
def nft_like(request, nft_id):
    nft = get_object_or_404(NFT, id=nft_id)
    like, created = Like.objects.get_or_create(nft=nft, user=request.user)
    
    if not created:
        like.delete()
        return JsonResponse({'status': 'unliked'})
    
    return JsonResponse({'status': 'liked'})


@login_required
def auction_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    nft = auction.nft

    user_wallet = Wallet.objects.filter(user=request.user, blockchain=nft.blockchain).first()
    if not user_wallet:
        messages.error(request, f"You don't have a wallet associated with {nft.blockchain} blockchain.")
        return redirect(f"{reverse('wallet:connect')}?next={request.path}")
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user
            bid.save()
            messages.success(request, f"You have successfully place a bid to {nft.name}.")
            return redirect('collection:auction_detail', nft.id, auction.id)
    else:
        form = BidForm()
    
    context = {
        'nft': nft,
        'auction': auction,
        'form': form, 
    }
    
    return render(request, 'nft-bid.html', context)


@login_required
def auction_purchase(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    nft = auction.nft
    wallet = Wallet.objects.filter(user=request.user, blockchain=nft.blockchain).first()

    if not wallet:
        messages.error(request, f"You don't have a wallet associated with {nft.blockchain} blockchain.")
        return redirect(f"{reverse('wallet:connect')}?next={request.path}")

    if wallet.balance < auction.price:
        messages.error(request, "You don't have enough funds to purchase this NFT.")
        return redirect('collection:auction_detail', nft.id, auction.id)

    wallet.balance -= auction.price
    wallet.save()

    nft.collectors.add(request.user)

    messages.success(request, f"You have successfully purchased {nft.name}.")
    return redirect('collection:nft_detail', nft.id)
