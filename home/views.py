from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Faq
from collection.models import NFT, Auction
from users.models import User, Avatar


def home_view(request):
    now = timezone.now()
    ending_auction = Auction.objects.filter(end_time__gt=now, start_time__lte=now).order_by('end_time').first()
    top_nfts = NFT.objects.annotate(like_count=Count('likes')).filter(collections__isnull=False).order_by('-like_count')[:4]
    faqs = Faq.objects.all()[:3]
    staff_users = User.objects.filter(is_staff=True)[:3]
    avatars = Avatar.objects.all()[:3]

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

    context = {
        'auction': ending_auction,
        'top_nfts': top_nfts,
        'faqs': faqs,
        'staff_users': staff_users,
        'avatars': avatars,
        'top_collectors_1': top_collectors_1,
        'top_collectors_2': top_collectors_2,
    }   

    return render(request, 'index.html', context)


def roadmap_view(request):
    faqs = Faq.objects.all()[:3]
    staff_users = User.objects.filter(is_staff=True)[:3]

    context = {
        'faqs': faqs,
        'staff_users': staff_users,
    }
    return render(request, 'roadmap.html', context)


def ourclans_view(request):
    faqs = Faq.objects.all()[:3]

    context = {
        'faqs': faqs,
    }
    return render(request, 'ourclans.html', context)


def faq_view(request):
    faqs = Faq.objects.all()

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

    context = {
        'faqs': faqs,
        'top_collectors_1': top_collectors_1,
        'top_collectors_2': top_collectors_2,
    }
    return render(request, 'faq.html', context)