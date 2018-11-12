from django.core.paginator import Paginator
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.parsers import JSONParser

from utils.response_util import response

from rest_framework.generics import ListAPIView, CreateAPIView
from data.constants import RATE_TIME, VERSION_APP, PAGING_ITEM, PAKAGE_APP
from user.serializer import UserFavoriteDetailSerializer
from data.models import FavoriteSongModel


class UserFavoriteDetailController(ListAPIView, CreateAPIView):
    serializer_class = UserFavoriteDetailSerializer

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def list(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        page = 1
        user_id = kwargs['pk']
        if 'page' in request.GET:
            page = request.GET['page']
        user_song = FavoriteSongModel.objects.filter(user_id=user_id).distinct()
        if user_song and user_song.count() > 0:
            p = Paginator(user_song, PAGING_ITEM)
            total_item = user_song.count()
            total_page = p.num_pages
            serializer = self.get_serializer(instance=p.page(page).object_list, many=True).data
            return response({'data': serializer,
                             'total_item': total_item,
                             'total_page': total_page, 'current_page': page},
                            status=status.HTTP_200_OK)
        return response({}, status=status.HTTP_404_NOT_FOUND)

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def post(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        user_id = kwargs['pk']
        data = JSONParser().parse(request)
        song_id = data['id']
        favorite = FavoriteSongModel.objects.filter(user_id=user_id, song_id=song_id)
        if favorite and favorite.count() > 0:
            favorite.delete()
            return response({}, status=status.HTTP_200_OK)
        else:
            FavoriteSongModel.objects.create(user_id=user_id, song_id=song_id)
            return response({}, status=status.HTTP_201_CREATED)
