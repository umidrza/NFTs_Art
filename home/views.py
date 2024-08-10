from django.shortcuts import render
from collection.models import NFT, Auction
from django.utils import timezone
from django.db.models import Count


def home_view(request):
    now = timezone.now()
    ending_auction = Auction.objects.filter(end_time__gt=now, start_time__lte=now).order_by('end_time').first()
    top_nfts = NFT.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:4]

    context = {
        'auction': ending_auction,
        'top_nfts': top_nfts,
    }

    return render(request, 'index.html', context)


def roadmap_view(request):
    return render(request, 'roadmap.html')


def ourclans_view(request):
    return render(request, 'ourclans.html')


def faq_view(request):
    return render(request, 'faq.html')