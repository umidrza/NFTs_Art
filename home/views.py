from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Faq
from collection.models import NFT, Auction
from users.models import User


def home_view(request):
    now = timezone.now()
    ending_auction = Auction.objects.filter(end_time__gt=now, start_time__lte=now).order_by('end_time').first()
    top_nfts = NFT.objects.annotate(like_count=Count('likes')).filter(collections__isnull=False).order_by('-like_count')[:4]
    faqs = Faq.objects.all()[:3]
    staff_users = User.objects.filter(is_staff=True)[:3]

    context = {
        'auction': ending_auction,
        'top_nfts': top_nfts,
        'faqs': faqs,
        'staff_users': staff_users,
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

    context = {
        'faqs': faqs,
    }
    return render(request, 'faq.html', context)