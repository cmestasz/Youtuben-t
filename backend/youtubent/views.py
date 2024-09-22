from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files import File
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import os
import requests
import yt_dlp
from .models import CachedAudio, Account, AccountAudio, Session
from .serializers import CachedAudioSerializer
from .utils import download_song, refresh_downloads, refresh_session, dumb_token, clean_cache
from .consts import MAX_SAVED_VIDEOS, BASE_MEDIA_URL, HOURS_DOWNLOADS_RESET, MAX_DOWNLOADS

# Create your views here.


class Login(APIView):
    def post(self, request):
        type = request.data['type']
        if type == 'token':
            token = request.data['token']
            if token:
                session = Session.objects.filter(token=token).first()
                if session:
                    if session.expire < timezone.now():
                        session.delete()
                        return Response({'error': 'Token expired'}, status=400)

                    refresh_session(session)
                    return Response({'token': token, 'user': session.account.user}, status=200)
            return Response({'error': 'Invalid token'}, status=400)

        elif type == 'credentials':
            user = request.data['user']
            password = request.data['password']
            if user and password:
                account = Account.objects.filter(user=user).first()
                if account and check_password(password, account.password):
                    Session.objects.filter(account=account).delete()

                    token = dumb_token()
                    session = Session.objects.create(
                        token=token, account=account)
                    refresh_session(session)
                    return Response({'token': token, 'user': session.account.user}, status=200)

                return Response({'error': 'User and password don\'t match'}, status=400)
            return Response({'error': 'Invalid user or password'}, status=400)


class Register(APIView):
    def post(self, request):
        user = request.data['user']
        password = request.data['password']

        if user and password:
            if Account.objects.filter(user=user).exists():
                return Response({'error': 'User already exists'}, status=400)

            h_password = make_password(password)
            account = Account.objects.create(user=user, password=h_password)

            token = dumb_token()
            session = Session.objects.create(account=account, token=token)
            refresh_session(session)

            return Response({'token': token, 'user': account.user}, status=200)

        return Response({'error': 'Invalid user or password'}, status=400)


class Logout(APIView):
    def post(self, request):
        token = request.data['token']
        if token:
            session = Session.objects.filter(token=token).first()
            if session:
                session.delete()
                return Response({}, status=200)
        return Response({'error': 'Invalid token'}, status=400)


class Search(APIView):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
    MAX_RESULTS = 10

    def post(self, request):
        clean_cache()

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
            return Response({'error': "Either invalid token or the token used up its 100 daily searches, generate another token."}, status=400)
        return Response({'error': 'Invalid query or token (duh)'}, status=400)


class Play(APIView):
    def post(self, request):
        clean_cache()
        video_id = request.data['video_id']
        token = request.data['token']

        sessions = Session.objects.filter(token=token)
        if token and video_id and sessions.exists():
            account = sessions.first().account

            refresh_downloads(account)
            
            audio_objs = CachedAudio.objects.filter(yt_id=video_id)

            if audio_objs.exists():
                audio_obj = audio_objs.first()

                if audio_obj.file:
                    return Response({'url': BASE_MEDIA_URL + audio_obj.file.url}, status=200)

                if account.downloads_count < MAX_DOWNLOADS or account.special:
                    ok, message = download_song(video_id, BASE_MEDIA_URL, audio_obj)
                    if ok:
                        account.downloads_count += 1
                        account.save()
                        return Response({'url': message}, status=200)
                    return Response({'error': message}, status=400)
                
                return Response({'error': 'You have reached the maximum amount of hourly downloads'}, status=400)
            return Response({'error': 'Video not found'}, status=400)
        return Response({'error': 'Invalid token or video_id'}, status=400)


class CachedAudioViewSet(APIView):
    def get(self, request):
        queryset = CachedAudio.objects.exclude(file='')
        serializer = CachedAudioSerializer(queryset, many=True)
        return Response(serializer.data)


class Save(APIView):
    def post(self, request):
        token = request.data['token']
        video_id = request.data['video_id']

        if token and video_id:
            session = Session.objects.filter(token=token).first()
            if session:
                account = session.account

                refresh_downloads(account)

                audio = CachedAudio.objects.filter(yt_id=video_id).first()
                if audio:
                    if account.saved_amount < MAX_SAVED_VIDEOS:
                        existing = AccountAudio.objects.filter(account=account, audio=audio)
                        if not existing.exists():
                            if audio.file:
                                return Response({'url': BASE_MEDIA_URL + audio.file.url}, status=200)

                            if account.downloads_count < MAX_DOWNLOADS or account.special:
                                AccountAudio.objects.create(account=account, audio=audio)
                                account.downloads_count += 1
                                account.saved_amount += 1
                                account.save()
                                ok, message = download_song(video_id, BASE_MEDIA_URL, audio)
                                if ok:
                                    return Response({'url': message}, status=200)
                                return Response({'error': message}, status=400)
                            return Response({'error': 'You have reached the maximum amount of hourly downloads'}, status=400)
                        return Response({'error': 'Video already saved'}, status=400)
                    return Response({'error': 'You have reached the maximum amount of saved videos'}, status=400)
        return Response({'error': 'Invalid token or video_id'}, status=400)


class Forget(APIView):
    def post(self, request):
        token = request.data['token']
        video_id = request.data['video_id']

        if token and video_id:
            session = Session.objects.filter(token=token).first()
            if session:
                account = session.account
                audio = CachedAudio.objects.filter(yt_id=video_id).first()
                if audio:
                    query = AccountAudio.objects.filter(
                        account=account, audio=audio)
                    if query.exists():
                        query.delete()
                        account.saved_amount -= 1
                        account.save()
                        return Response({}, status=200)
        return Response({'error': 'Invalid token or video_id'}, status=400)


class SavedList(APIView):
    def post(self, request):
        token = request.data['token']

        if token:
            session = Session.objects.filter(token=token).first()
            if session:
                account = session.account
                account_audios = AccountAudio.objects.filter(account=account)
                queryset = CachedAudio.objects.filter(accountaudio__in=account_audios)

                results = []
                for audio in queryset:
                    audio_serialized = {
                        'yt_id': audio.yt_id,
                        'title': audio.title,
                        'thumbnail': audio.thumbnail,
                        'channel': audio.channel,
                        'url': BASE_MEDIA_URL + audio.file.url
                    }
                    results.append(audio_serialized)

                data = {'results': results, 'saved_amount': account.saved_amount, 'max_amount': MAX_SAVED_VIDEOS}
                return Response(data, status=200)
        return Response({'error': 'Invalid token'}, status=400)
