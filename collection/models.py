from django.db import models
from django.conf import settings
from django.utils import timezone
from wallet.models import Blockchain


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
class Collection(models.Model):
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='collections', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.SET_NULL, null=True)
    nfts = models.ManyToManyField('NFT', related_name='collections', blank=True)

    def __str__(self):
        return self.name


class NFT(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    image = models.ImageField(upload_to='nfts/')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_nfts')
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    collectors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='nfts', blank=True)

    def __str__(self):
        return self.name
    
    def get_status(self, auction=None):
        if self.auctions.exists():
            if not auction:
                auction = self.auctions.order_by('start_time').first()
            if auction.start_time > timezone.now():
                return 'not-started'
            elif auction.end_time > timezone.now():
                return 'auction'
            else:
                return 'expired'
        else:
            return 'not-on-sale'
        

class Auction(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='auctions')
    saler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Auction of {self.nft.name}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Bid of {self.amount} by {self.bidder} on {self.auction.nft.name}"

class Like(models.Model):
    nft = models.ForeignKey(NFT, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nft', 'user')

    def __str__(self):
        return f"{self.user} likes {self.nft.name}"
    
