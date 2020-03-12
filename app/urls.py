from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url
#from .views import HelloView
from .views import *

urlpatterns = [
    #path("", HelloView.as_view(), name="index"),
    #path("", views.index, name="index"),
    path("", views.info_get, name="info_get"),
    path("friend_friend_rank_asc/", views.friend_friend_rank_asc, name="friend_friend_rank_asc"),
    path("friend_friend_rank_desc/", views.friend_friend_rank_desc, name="friend_friend_rank_desc"),
    path("friend_follower_rank_asc/", views.friend_follower_rank_asc, name="friend_follower_rank_asc"),
    path("friend_follower_rank_desc/", views.friend_follower_rank_desc, name="friend_follower_rank_desc"),
    path("friend_ratio_rank_asc/", views.friend_ratio_rank_asc, name="friend_ratio_rank_asc"),
    path("friend_ratio_rank_desc/", views.friend_ratio_rank_desc, name="friend_ratio_rank_desc"),
    path("follower_friend_rank_asc/", views.follower_friend_rank_asc, name="follower_friend_rank_asc"),
    path("follower_friend_rank_desc/", views.follower_friend_rank_desc, name="follower_friend_rank_desc"),
    path("follower_follower_rank_asc/", views.follower_follower_rank_asc, name="follower_follower_rank_asc"),
    path("follower_follower_rank_desc/", views.follower_follower_rank_desc, name="follower_follower_rank_desc"),
    path("follower_ratio_rank_asc/", views.follower_ratio_rank_asc, name="follower_ratio_rank_asc"),
    path("follower_ratio_rank_desc/", views.follower_ratio_rank_desc, name="follower_ratio_rank_desc"),

    path("select_friend/", views.select_friend, name="select_friend"),
    path("select_follower/", views.select_follower, name="select_follower"),
    path("", views.index, name="index"),
    # path("rank_friend/", views.rank_friend, name="rank_friend"),
    # path("rank_follower/", views.rank_follower, name="rank_follower"),
    # path("rank_ratio/", views.rank_ratio, name="rank_ratio"),
]
