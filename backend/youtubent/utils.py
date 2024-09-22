import os
import random
import string
from django.conf import settings
from django.utils import timezone
from django.core.files import File
import yt_dlp
from .models import AccountAudio, CachedAudio
from .consts import DAYS_FILE_EXPIRE, MINUTES_NO_FILE_EXPIRE, HOURS_DOWNLOADS_RESET


def dumb_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=50))


def refresh_session(session):
    session.expire = timezone.now() + timezone.timedelta(days=7)
    session.save()


def clean_cache():
    audios = CachedAudio.objects.all()
    for audio in audios:
        if (not AccountAudio.objects.contains(audio)):
            if (audio.file and timezone.now() - audio.created_at > timezone.timedelta(days=DAYS_FILE_EXPIRE)):
                audio.file.delete()
                audio.delete()
            elif (not audio.file and timezone.now() - audio.created_at > timezone.timedelta(minutes=MINUTES_NO_FILE_EXPIRE)):
                audio.delete()

def refresh_downloads(account):
    if timezone.now() - account.downloads_reset > timezone.timedelta(hours=HOURS_DOWNLOADS_RESET):
        account.downloads_reset = timezone.now()
        account.downloads_count = 0
        account.save()

def download_song(yt_id, base_url, audio_obj):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'temp/{yt_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(
            [f'https://www.youtube.com/watch?v={yt_id}'])

        if error_code:
            return (False, 'The library failed, tell the creator to update it')

    try:
        route = os.path.join(
            settings.BASE_DIR, 'temp', f'{yt_id}.m4a')

        with open(route, 'rb') as file:
            django_file = File(file, name=f'{yt_id}.m4a')

            audio_obj.file = django_file
            audio_obj.save()

            django_file.close()

        os.remove(route)
        url = base_url + audio_obj.file.url
        return (True, url)
    except Exception as e:
        print(e)
        return (False, 'Too lazy to test this, tell the creator')
