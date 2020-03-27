from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url
#from .views import HelloView
from .views import *

urlpatterns = [
    path("", views.info_get, name="info_get"),
    path("select/",views.select, name="select"),
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
    path("", views.index, name="index"),
]
