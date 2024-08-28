from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Faq
from collection.models import NFT, Auction
from users.models import User, Avatar
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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


def get_in_touch(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            name = request.user.fullname if request.user.is_authenticated else 'Subscriber'
            html_message = render_to_string('partials/subscriber-email.html', {'name': name})
            email_message = EmailMessage(
                subject = 'NFTs Art Newsletter',
                body = html_message,
                from_email = settings.EMAIL_HOST_USER,
                to = [email],
            )
            email_message.content_subtype = 'html'
            email_message.send()

            messages.success(request, 'Email sent successfully!')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect('home:faq')