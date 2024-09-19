from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from .models import CachedAudio

class CachedAudioSerializer(ModelSerializer):
    class Meta:
        model = CachedAudio
        fields = ['title', 'yt_id', 'thumbnail', 'channel']

class CachedAudioViewSet(ModelViewSet):
    queryset = CachedAudio.objects.all()
    serializer_class = CachedAudioSerializer
