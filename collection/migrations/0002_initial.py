# Generated by Django 5.0.7 on 2024-08-26 13:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0001_initial'),
        ('wallet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='saler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='collection.auction'),
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='blockchain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wallet.blockchain'),
        ),
        migrations.AddField(
            model_name='collection',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='collection.category'),
        ),
        migrations.AddField(
            model_name='collection',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auction',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.currency'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nft',
            name='blockchain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.blockchain'),
        ),
        migrations.AddField(
            model_name='nft',
            name='collectors',
            field=models.ManyToManyField(blank=True, related_name='nfts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nft',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_nfts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='nft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='collection.nft'),
        ),
        migrations.AddField(
            model_name='collection',
            name='nfts',
            field=models.ManyToManyField(blank=True, related_name='collections', to='collection.nft'),
        ),
        migrations.AddField(
            model_name='auction',
            name='nft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='collection.nft'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('nft', 'user')},
        ),
    ]
