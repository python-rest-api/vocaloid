from django.core.paginator import Paginator
from ratelimit.decorators import ratelimit
from rest_framework import status

from utils.response_util import response

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from data.constants import RATE_TIME, VERSION_APP, PAGING_ITEM, PAKAGE_APP
from song.serializer import SongDetailSerializer
from data.models import SongModel


class SongController(ListAPIView):
    serializer_class = SongDetailSerializer

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def list(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        if 'name' in request.GET:
            songs = SongModel.objects.filter(name__icontains=request.GET['name']) \
                .order_by('name')
        else:
            songs = SongModel.objects.filter().order_by('name')
        if songs.count() > 0:
            p = Paginator(songs, PAGING_ITEM)
            total_item = songs.count()
            total_page = p.num_pages
            serializer = self.get_serializer(instance=p.page(page).object_list, many=True).data
            return response({'data': serializer,
                             'total_item': total_item,
                             'total_page': total_page, 'current_page': page},
                            status=status.HTTP_200_OK)
        return response({}, status=status.HTTP_404_NOT_FOUND)


class SongDetailController(UpdateAPIView):

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def put(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        song_id = kwargs['pk']
        song = SongModel.objects.filter(id=song_id)

        if song.count() <= 0:
            return response({}, status=status.HTTP_406_NOT_ACCEPTABLE)
        t_view = song[0].view
        total_view = t_view + 1
        song.update(view=total_view)
        return response({}, status=status.HTTP_200_OK)


class SongAdminController(CreateAPIView):
    serializer_class = SongDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)