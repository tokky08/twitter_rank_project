from django.db import models

# Create your models here.
class User_Info(models.Model):
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

    def __str__(self):
        return str(self.screen_name) + "/" + str(self.user_id)
    


