from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Blockchain(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class NFT(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='nfts/')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=20)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='collections', on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collection_followers', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nfts = models.ManyToManyField(NFT, related_name='collections', blank=True)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AuctionNFT(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction of {self.nft.name}"
