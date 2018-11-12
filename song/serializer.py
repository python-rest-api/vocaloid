from rest_framework import serializers
from data.models import SongModel, SingerSongModel, SingerModel


class SongDetailSerializer(serializers.ModelSerializer):
    singer = serializers.SerializerMethodField('get_singer_song')

    def get_singer_song(self, borrower):
        if borrower is not None:
            singername = ""
            lstsinger = SingerSongModel.objects.filter(song_id=borrower.id)
            for ss in lstsinger:
                if singername:
                    singername += " ," + SingerModel.objects.get(id=ss.singer_id).name
                else:
                    singername += SingerModel.objects.get(id=ss.singer_id).name
            return singername
        return None

    class Meta:
        model = SongModel
        fields = ('id', 'create_date', 'name', 'link', 'thumbnail', 'duration', 'view', 'singer')
