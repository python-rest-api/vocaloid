from django.core.paginator import Paginator
from ratelimit.decorators import ratelimit
from rest_framework import status
from utils.response_util import response

from rest_framework.generics import ListAPIView, CreateAPIView
from data.constants import RATE_TIME, VERSION_APP, PAGING_ITEM, PAKAGE_APP
from singer.serializer import SingerDetailSerializer, SingerSongDetailSerializer
from data.models import SingerModel, SingerSongModel


class SingerController(ListAPIView):
    serializer_class = SingerDetailSerializer

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
            singers = SingerModel.objects.filter(name__icontains=request.GET['name']) \
                .order_by('-create_date')
        else:
            singers = SingerModel.objects.filter().order_by('-create_date')
        if singers.count() > 0:
            p = Paginator(singers, PAGING_ITEM)
            total_item = singers.count()
            total_page = p.num_pages
            serializer = self.get_serializer(instance=p.page(page).object_list, many=True).data
            return response({'data': serializer,
                             'total_item': total_item,
                             'total_page': total_page, 'current_page': page},
                            status=status.HTTP_200_OK)
        return response({}, status=status.HTTP_404_NOT_FOUND)


class SingerDetailController(ListAPIView):
    serializer_class = SingerSongDetailSerializer

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def list(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        singer_id = kwargs['pk']
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        singer_song = SingerSongModel.objects.filter(singer_id=singer_id).distinct()
        if singer_song and singer_song.count() > 0:
            p = Paginator(singer_song, PAGING_ITEM)
            total_item = singer_song.count()
            total_page = p.num_pages
            serializer = self.get_serializer(instance=p.page(page).object_list, many=True).data
            return response({'data': serializer,
                             'total_item': total_item,
                             'total_page': total_page, 'current_page': page},
                            status=status.HTTP_200_OK)
        return response({}, status=status.HTTP_404_NOT_FOUND)


class SingerAdminController(CreateAPIView):
    serializer_class = SingerDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
