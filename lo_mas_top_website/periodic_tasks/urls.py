from django.urls import path
from . import views

urlpatterns = [
    path(
        route= 'youtube', 
        view= views.run_youtube_task,
        name='youtube'
    )
]