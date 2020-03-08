from django.db import models

# Create your models here.
class User_Info(models.Model):
    profile_image_url_https = models.CharField(max_length=100)  #アイコン画像
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    ratio = models.FloatField(default=0)

class Relation_Info(models.Model):
    following = models.CharField(max_length=100)
    followed = models.CharField(max_length=100)




class Friend_Info(models.Model):
    my_screen_name = models.CharField(max_length=100, null=True)
    profile_image_url_https = models.CharField(max_length=100) #アイコン画像
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    ratio = models.FloatField(default=0)
    statuses_count = models.IntegerField(default=0) #ツイート数
    created_at = models.DateField() #アカウントの作成日時
    description = models.CharField(max_length=100) #プロフィール文の詳細文
    favourites_count = models.IntegerField(default=0)  #自分がお気に入りしたツイートの数


class Follower_Info(models.Model):
    my_screen_name = models.CharField(max_length=100, null=True)
    profile_image_url_https = models.CharField(max_length=100) #アイコン画像
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    ratio = models.FloatField(default=0)
    statuses_count = models.IntegerField(default=0) #ツイート数
    created_at = models.DateField() #アカウントの作成日時
    description = models.CharField(max_length=100) #プロフィール文の詳細文
    favourites_count = models.IntegerField(default=0)  #自分がお気に入りしたツイートの数