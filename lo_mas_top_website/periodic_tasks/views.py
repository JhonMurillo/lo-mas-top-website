#Server
from django.http import HttpResponse, JsonResponse
from http import HTTPStatus
from .youtube.scraper import get_data

def run_youtube_task(request):
    get_data()
    return JsonResponse({
                'message': 'Task Youtube schedule...'
            }, status=HTTPStatus.OK)