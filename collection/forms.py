from django import forms
from .models import NFT, Auction, Collection


class NFTForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = NFT
        fields = ['name', 'description', 'image', 'blockchain', 'collections']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['collections'].queryset = Collection.objects.filter(creator=user)


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['price', 'currency', 'start_time', 'end_time', 'quantity']


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['blockchain', 'name', 'category']