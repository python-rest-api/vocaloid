from django.conf.urls import url

from user.controller import UserFavoriteDetailController

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/songs$', UserFavoriteDetailController.as_view()),
]