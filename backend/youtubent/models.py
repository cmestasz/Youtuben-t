from django.db import models

# Create your models here.
class CachedAudio(models.Model):
    yt_id = models.CharField(max_length=30, primary_key=True)
    file = models.FileField(upload_to='audio/')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)