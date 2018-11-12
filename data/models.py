from django.db import models


class UserModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=True, default=None, max_length=100)
    fb = models.CharField(null=True, default=None, max_length=200)
    avatar = models.TextField(null=True, default=None, max_length=200)

    class Meta:
        db_table = "user"


class SingerModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    avatar = models.CharField(null=True, default=None, max_length=200)

    class Meta:
        db_table = "singer"


class SongModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    duration = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    favorite = models.ManyToManyField(UserModel, through='FavoriteSongModel',
                                      through_fields=('song', 'user'))
    auth = models.ManyToManyField(SingerModel, through='SingerSongModel',
                                  through_fields=('song', 'singer'))

    class Meta:
        db_table = "song"


class ShowModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    download = models.IntegerField(default=0)
    type_ads = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "show"


class FavoriteSongModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                             related_name='favorite_song_id_user')
    song = models.ForeignKey(SongModel, on_delete=models.CASCADE,
                             related_name='favorite_song_id_song')

    class Meta:
        db_table = "favorite_song"


class SingerSongModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    singer = models.ForeignKey(SingerModel, on_delete=models.CASCADE,
                               related_name='singer_song_id_singer')
    song = models.ForeignKey(SongModel, on_delete=models.CASCADE,
                             related_name='singer_song_id_song')

    class Meta:
        db_table = "singer_song"
