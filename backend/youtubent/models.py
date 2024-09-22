from django.db import models

# Create your models here.


class CachedAudio(models.Model):
    yt_id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    channel = models.CharField(max_length=100)
    file = models.FileField(upload_to='audio/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    user = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    saved_amount = models.IntegerField(default=0)
    downloads_reset = models.DateTimeField(auto_now_add=True)
    downloads_count = models.IntegerField(default=0)
    special = models.BooleanField(default=False)


class AccountAudio(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    audio = models.ForeignKey(CachedAudio, on_delete=models.CASCADE)


class Session(models.Model):
    token = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    expire = models.DateTimeField(auto_now_add=True)
