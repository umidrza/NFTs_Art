from django.contrib import admin
from .models import Category, Blockchain, NFT, Collection, AuctionNFT

admin.site.register(Category)
admin.site.register(Blockchain)
admin.site.register(NFT)
admin.site.register(Collection)
admin.site.register(AuctionNFT)