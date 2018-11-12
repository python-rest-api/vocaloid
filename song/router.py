from django.conf.urls import url

from song.controller import SongDetailController

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)$', SongDetailController.as_view()),
]