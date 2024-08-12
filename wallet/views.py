from django.shortcuts import render, redirect
from .models import Wallet, Provider, Blockchain
from .forms import WalletForm
import random


def connect_wallet(request):
    providers = Provider.objects.all()
    blockchains = Blockchain.objects.all()

    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            provider = form.cleaned_data['provider']
            blockchain = form.cleaned_data['blockchain']

            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                provider=provider,
                blockchain=blockchain,
                defaults={'key': ''.join(random.choices('0123456789', k=15))}
            )

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                redirect_url = f"{next_url}?wallet_id={wallet.id}"
                return redirect(redirect_url)
            else:
                return redirect('home')
            
    else:
        form = WalletForm()


    context = {
        'providers': providers,
        'blockchains': blockchains,
        'form': form,
    }

    return render(request, 'connect-wallet.html', context)
