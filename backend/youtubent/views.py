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
from .utils import refresh_session, dumb_token
from .consts import MAX_SAVED_VIDEOS

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

        print(user, password)
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


class Save(APIView):
    def post(self, request):
        token = request.data['token']
        video_id = request.data['video_id']

        if token and video_id:
            session = Session.objects.filter(token=token).first()
            if session:
                account = session.account
                audio = CachedAudio.objects.filter(yt_id=video_id).first()
                if audio:
                    if account.saved_amount < MAX_SAVED_VIDEOS:
                        existing = AccountAudio.objects.filter(account=account, audio=audio)
                        if not existing.exists():
                            AccountAudio.objects.create(account=account, audio=audio)
                            account.saved_amount += 1
                            account.save()
                            return Response({}, status=200)
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

                serializer = CachedAudioSerializer(queryset, many=True)
                
                data = {'results': serializer.data, 'saved_amount': account.saved_amount, 'max_amount': MAX_SAVED_VIDEOS}
                return Response(data, status=200)
        return Response({'error': 'Invalid token'}, status=400)
