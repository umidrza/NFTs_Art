from django import forms
from .models import NFT, Auction

class NFTForm(forms.ModelForm):
    class Meta:
        model = NFT
        fields = ['name', 'description', 'image', 'blockchain']


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['price', 'currency', 'start_time', 'end_time', 'quantity']