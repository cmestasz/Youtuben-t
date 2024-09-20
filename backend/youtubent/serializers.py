from rest_framework.serializers import ModelSerializer
from .models import CachedAudio

class CachedAudioSerializer(ModelSerializer):
    class Meta:
        model = CachedAudio
        fields = ['title', 'yt_id', 'thumbnail', 'channel']