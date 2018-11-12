from rest_framework import status
from ratelimit.decorators import ratelimit
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser

from data.constants import RATE_TIME, VERSION_APP, PAKAGE_APP
from user.serializer import UserDetailSerializer
from utils.facebook_util import get_facebook_profile
from utils.response_util import response
from data.models import UserModel


class AuthController(CreateAPIView):
    serializer_class = UserDetailSerializer

    @ratelimit(key='ip', rate=RATE_TIME, block=True)
    def post(self, request, *args, **kwargs):
        version = request.META['HTTP_VERSION']
        pakage = request.META['HTTP_PAKAGE']
        if int(version) < VERSION_APP or pakage != PAKAGE_APP:
            return response({}, status=status.HTTP_403_FORBIDDEN)
        data = JSONParser().parse(request)
        profile = get_facebook_profile(data['access_token'])
        if profile and 'id' in profile:
            fb = 'https://www.facebook.com/' + profile['id']
            user = UserModel.objects.filter(fb=fb)
            if user.count() > 0:
                ret_data = UserDetailSerializer(instance=user[0]).data
                return response({"data": ret_data}, status=status.HTTP_200_OK)
            else:
                try:
                    avatar = profile['picture']['data']['url']
                except:
                    avatar = ""
                fb = 'https://www.facebook.com/' + profile['id']
                user = UserModel.objects.create(fb=fb, name=profile['name'], avatar=avatar)
                ret_data = UserDetailSerializer(instance=user).data
                return response({"data": ret_data}, status=status.HTTP_201_CREATED)
        return response({}, status=status.HTTP_404_NOT_FOUND)
