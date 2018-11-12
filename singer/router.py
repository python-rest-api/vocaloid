from django.conf.urls import url

from singer.controller import SingerDetailController

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/songs$', SingerDetailController.as_view()),
]
