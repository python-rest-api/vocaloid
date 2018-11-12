from rest_framework import serializers
from data.models import UserModel, SingerSongModel, SingerModel


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class UserFavoriteDetailSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id_song')
    create_date = serializers.SerializerMethodField('get_create_date_song')
    name = serializers.SerializerMethodField('get_name_song')
    link = serializers.SerializerMethodField('get_link_song')
    thumbnail = serializers.SerializerMethodField('get_thumbnail_song')
    duration = serializers.SerializerMethodField('get_duration_song')
    view = serializers.SerializerMethodField('get_total_view_song')
    singer = serializers.SerializerMethodField('get_singer_song')

    def get_id_song(self, borrower):
        if borrower is not None:
            return borrower.song.id
        return None

    def get_create_date_song(self, borrower):
        if borrower is not None:
            return borrower.song.create_date
        return None

    def get_name_song(self, borrower):
        if borrower is not None:
            return borrower.song.name
        return None

    def get_link_song(self, borrower):
        if borrower is not None:
            return borrower.song.link
        return None

    def get_thumbnail_song(self, borrower):
        if borrower is not None:
            return borrower.song.thumbnail
        return None

    def get_duration_song(self, borrower):
        if borrower is not None:
            return borrower.song.duration
        return None

    def get_total_view_song(self, borrower):
        if borrower is not None:
            return borrower.song.view
        return None

    def get_singer_song(self, borrower):
        if borrower is not None:
            singername = ""
            lstsinger = SingerSongModel.objects.filter(song_id=borrower.song.id)
            for ss in lstsinger:
                if singername:
                    singername += " ," + SingerModel.objects.get(id=ss.singer_id).name
                else:
                    singername += SingerModel.objects.get(id=ss.singer_id).name
            return singername
        return None

    class Meta:
        model = UserModel
        fields = ('id', 'create_date', 'name', 'link', 'thumbnail', 'duration', 'view', 'singer')
