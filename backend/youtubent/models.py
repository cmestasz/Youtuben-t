from django.db import models

# Create your models here.
class CachedAudio(models.Model):
    yt_id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    channel = models.CharField(max_length=100)
    file = models.FileField(upload_to='audio/', null=True)
    