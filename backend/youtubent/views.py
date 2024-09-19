from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files import File
from django.conf import settings
import os
import requests
import yt_dlp
from .models import CachedAudio
from .serializers import CachedAudioSerializer

# Create your views here.


class Search(APIView):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
    MAX_RESULTS = 10

    def post(self, request):
        query = request.data['query']
        token = request.data['token']

        if query and token:
            url = f'{self.BASE_URL}?part=snippet&q={query}&key={
                token}&maxResults={self.MAX_RESULTS}'
            get = requests.get(url)

            if get.status_code == 200:
                data = get.json()
                results = []
                for item in data['items']:
                    if (item['id']['kind'] == 'youtube#video'):
                        title = item['snippet']['title']
                        yt_id = item['id']['videoId']
                        thumbnail = item['snippet']['thumbnails']['default']['url']
                        channel = item['snippet']['channelTitle']

                        CachedAudio.objects.get_or_create(
                            yt_id=yt_id,
                            title=title,
                            thumbnail=thumbnail,
                            channel=channel
                        )

                        results.append({
                            'yt_id': yt_id,
                            'title': title,
                            'thumbnail': thumbnail,
                            'channel': channel
                        })

                return Response({'results': results}, status=200)
            return Response({'error': "Youtube didn't like that, default API keys give you 100 queries per day, generate another one and set it"}, status=400)
        return Response({'error': 'Invalid query or token (duh)'}, status=400)


class Play(APIView):
    BASE_URL = 'http://localhost:8000'

    def post(self, request):
        video_id = request.data['video_id']

        audio_objs = CachedAudio.objects.filter(yt_id=video_id)

        if video_id and audio_objs.exists():
            audio_obj = audio_objs.first()
            if audio_obj.file:
                url = f'{self.BASE_URL}{audio_obj.file.url}'
                return Response({'url': url}, status=200)

            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'outtmpl': f'temp/{video_id}.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(
                    [f'https://www.youtube.com/watch?v={video_id}'])

                if error_code:
                    return Response({'error': 'The library failed, tell the creator to update it'}, status=400)

            try:
                route = os.path.join(
                    settings.BASE_DIR, 'temp', f'{video_id}.m4a')

                with open(route, 'rb') as file:
                    django_file = File(file, name=f'{video_id}.m4a')

                    audio_obj.file = django_file
                    audio_obj.save()

                    django_file.close()

                os.remove(route)
                url = f'{self.BASE_URL}{audio_obj.file.url}'
                return Response({'url': url}, status=200)
            except Exception as e:
                print(e)
                return Response({'error': 'I was too lazy to test this, tell the creator'}, status=400)
        return Response({'error': 'Invalid video_id'}, status=400)


class CachedAudioViewSet(APIView):
    def get(self, request):
        queryset = CachedAudio.objects.exclude(file='')
        serializer = CachedAudioSerializer(queryset, many=True)
        return Response(serializer.data)
