"""vocaloid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from auth.authentication import AuthController
from django.conf import settings
from django.conf.urls.static import static
from singer.controller import SingerAdminController, SingerController
from song.controller import SongAdminController, SongController

urlpatterns = [
    url(r'v1/auth$', AuthController.as_view()),

    url(r'v1/admin/singer$', SingerAdminController.as_view()),

    url(r'v1/admin/song$', SongAdminController.as_view()),

    url(r'v1/singers$', SingerController.as_view()),

    url(r'v1/singer/', include('singer.router')),

    url(r'v1/songs$', SongController.as_view()),

    url(r'v1/song/', include('song.router')),

    url(r'v1/user/', include('user.router')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
