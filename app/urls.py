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
    path("rank_friend/", views.rank_friend, name="rank_friend"),
    path("rank_follower/", views.rank_follower, name="rank_follower"),
    path("rank_ratio/", views.rank_ratio, name="rank_ratio"),
]
