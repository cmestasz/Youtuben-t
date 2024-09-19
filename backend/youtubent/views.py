from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.


class Search(APIView):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
    MAX_RESULTS = 10

    def post(self, request):
        query = request.data['query']
        token = request.data['token']

        if query and token:
            url = f'{self.BASE_URL}?part=snippet&q={query}&key={token}&maxResults={self.MAX_RESULTS}'
            get = requests.get(url)

            if get.status_code == 200:
                data = get.json()
                results = []
                for item in data['items']:
                    results.append({
                        'title': item['snippet']['title'],
                        'video_id': item['id']['videoId'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url'],
                        'channel': item['snippet']['channelTitle'],
                    })

                return Response({'results': results}, status=200)
            return Response({'error': "Youtube didn't like that, default API keys give you 100 queries per day, generate another one and set it"}, status=400)
        return Response({'error': 'Invalid query or token (duh)'}, status=400)

