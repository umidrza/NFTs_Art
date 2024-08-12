from django.db import models
from django.conf import settings
import random
from datetime import datetime, timedelta


class Blockchain(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='providers/')

    def __str__(self):
        return self.name

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    key = models.CharField(max_length=15, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = ''.join(random.choices('0123456789', k=15))
        if not self.expiration:
            self.expiration = datetime.now() + timedelta(days=3*365)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.provider.name} - {self.blockchain.name}'