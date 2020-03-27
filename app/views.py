from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm
import tweepy
# from .api_key import *
from .models import Friend_Info, Follower_Info
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.conf import settings

auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


####################################     フォローしている人での昇順/降順への並び替え     #########################################

##################       フォロー数     ##########################
def friend_friend_rank_asc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("friends_count")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)


def friend_friend_rank_desc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-friends_count")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)

##################       フォロワー数     ##########################


def friend_follower_rank_asc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("followers_count")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)


def friend_follower_rank_desc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-followers_count")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)

##################       比率        ##########################


def friend_ratio_rank_asc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("ratio")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)


def friend_ratio_rank_desc(request):
    response = {
        "screen_name": "",
        "friend": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["friend"] = Friend_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-ratio")
    response["rank"] = friend_rank(request, response["friend"])
    response["all_users_count"] = all_users_count(response["friend"])
    return render(request, "app/friend.html", response)

##################       順位       ##########################

#######    自分の順位     ###########
def friend_rank(request, friend):
    rank = 0
    for screen_name in friend:
        rank += 1
        if screen_name.screen_name == request.GET.get("screen_name"):
            break
    return rank

#######    何位中     ###########
def all_users_count(friend):
    rank = 0
    for screen_name in friend:
        rank += 1
    return rank


####################################     フォロワーでの昇順/降順への並び替え     #########################################


##################       フォロー数     ##########################
def follower_friend_rank_asc(request):
    response = {
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("friends_count")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)


def follower_friend_rank_desc(request):
    response = {
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-friends_count")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)

##################       フォロワー数     ##########################


def follower_follower_rank_asc(request):
    response = {
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("followers_count")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)


def follower_follower_rank_desc(request):
    response = {
        "my_self_info": "",
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-followers_count")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)

##################       比率        ##########################


def follower_ratio_rank_asc(request):
    response = {
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("ratio")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)


def follower_ratio_rank_desc(request):
    response = {
        "screen_name": "",
        "follower": "",
        "rank": 0,
        "all_users_count": 0,
    }
    response["screen_name"] = request.GET.get("screen_name")
    response["follower"] = Follower_Info.objects.filter(my_screen_name=response["screen_name"]).order_by("-ratio")
    response["rank"] = follower_rank(request, response["follower"])
    response["all_users_count"] = all_users_count(response["follower"])
    return render(request, "app/follower.html", response)

##################       順位       ##########################

#######    自分の順位     ###########
def follower_rank(request, follower):
    rank = 0
    for screen_name in follower:
        rank += 1
        if screen_name.screen_name == request.GET.get("screen_name"):
            break
    return rank

#######    何位中     ###########
def all_users_count(follower):
    rank = 0
    for screen_name in follower:
        rank += 1
    return rank


def index(request):
    return render(request, "app/index.html")

def select(request):
    return render(request, "app/select.html")



####################################     フォローしている人/フォロワーの全情報をDBに格納     #########################################

def info_get(request):

    user_info = {
        "screen_name": "",
        "my_self_info": "",
        "form": HelloForm(),
    }

    if (request.method == "POST"):

        user_info["screen_name"] = request.POST["screen_name"]
        user_info["my_self_info"] = api.get_user(screen_name=user_info["screen_name"])
        user_info["form"] = HelloForm(request.POST)

        user_counts = user_info["my_self_info"].friends_count + user_info["my_self_info"].followers_count

        if user_counts > 101:
            return render(request, "app/except.html")
            
        else:
            redirect_url = reverse('select')
            parameters = urlencode({'screen_name': user_info["screen_name"]})
            url = f'{redirect_url}?{parameters}'

            try:
                fridnd_info_save(request, user_info["screen_name"], user_info["my_self_info"])
                follower_info_save(request, user_info["screen_name"], user_info["my_self_info"])
                return redirect(url)

            except:
                return render(request, "app/except.html")


    else:
        return render(request, "app/index.html", user_info)


####################################     フォローしている人の情報をDBに格納     #########################################

def fridnd_info_save(request, my_screen_name, my_self_info):

    ############          フォローしている人の情報をlistにして取得          ###################
    friends_info_list = friends_info(my_screen_name, my_self_info)
    friends_icon_list = friend_icon(friends_info_list)
    friends_name_list = friend_name(friends_info_list)
    friends_screen_name_list = friend_screen_name(friends_info_list)
    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_friends_count_list = friend_friends_count(friends_info_list)
    friends_followers_count_list = friend_followers_count(friends_info_list)
    friends_ratio_list = friend_ratio(my_self_info, friends_info_list)

    #########     今回は使わないが追加したい時にコメントを外す     ###########
    # friends_statuses_count_list = friend_statuses_count(friends_info_list)
    # friends_created_at_list = friend_created_at(friends_info_list)
    # friends_description_list = friend_description(friends_info_list)
    # friends_favourites_count_list = friend_favourites_count(friends_info_list)

    # 前のデータを全消去する
    Friend_Info.objects.filter(my_screen_name=my_screen_name).delete()
    
    for i in range(my_self_info.friends_count + 1):

        friend_info = Friend_Info(
            my_screen_name=my_screen_name,
            profile_image_url_https=friends_icon_list[i],
            name=friends_name_list[i],
            screen_name=friends_screen_name_list[i],
            user_id=friends_ids_list[i],
            friends_count=friends_friends_count_list[i],
            followers_count=friends_followers_count_list[i],
            ratio=friends_ratio_list[i],

            #########     今回は使わないが追加したい時にコメントを外す     ###########
            # statuses_count=friends_statuses_count_list[i],
            # created_at=friends_created_at_list[i],
            # description=friends_description_list[i],
            # favourites_count=friends_favourites_count_list[i]
        )

        friend_info.save()


####################################     フォロワーの情報をDBに格納     #########################################

def follower_info_save(request, my_screen_name, my_self_info):

    ############          フォロワーの情報をlistにして取得          ###################
    followers_info_list = followers_info(my_screen_name, my_self_info)
    followers_icon_list = follower_icon(followers_info_list)
    followers_name_list = follower_name(followers_info_list)
    followers_screen_name_list = follower_screen_name(followers_info_list)
    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_friends_count_list = follower_friends_count(followers_info_list)
    followers_followers_count_list = follower_followers_count(followers_info_list)
    followers_ratio_list = follower_ratio(my_self_info, followers_info_list)

    #########     今回は使わないが追加したい時にコメントを外す     ###########
    # followers_statuses_count_list = follower_statuses_count(followers_info_list)
    # followers_created_at_list = follower_created_at(followers_info_list)
    # followers_description_list = follower_description(followers_info_list)
    # followers_favourites_count_list = follower_favourites_count(followers_info_list)

    # 前のデータを全消去する
    Follower_Info.objects.filter(my_screen_name=my_screen_name).delete()

    for i in range(my_self_info.followers_count + 1):

        follower_info = Follower_Info(
            my_screen_name=my_screen_name,
            profile_image_url_https=followers_icon_list[i],
            name=followers_name_list[i],
            screen_name=followers_screen_name_list[i],
            user_id=followers_ids_list[i],
            friends_count=followers_friends_count_list[i],
            followers_count=followers_followers_count_list[i],
            ratio=followers_ratio_list[i],

            #########     今回は使わないが追加したい時にコメントを外す     ###########
            # statuses_count=followers_statuses_count_list[i],
            # created_at=followers_created_at_list[i],
            # description=followers_description_list[i],
            # favourites_count=followers_favourites_count_list[i]
        )

        follower_info.save()


####################################     フォローしている人の情報取得     #########################################

##########   フォローしている人達の情報をlistに格納   ##########
def friends_info(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_info_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_info_list.append(friend)

    return friends_info_list

##########   フォローしている人達のiconをlistに格納   ##########


def friend_icon(friends_info_list):

    friends_icon_list = []
    for friend_info in friends_info_list:
        friends_icon_list.append(friend_info.profile_image_url_https)

    return friends_icon_list


##########   フォローしている人達のnameをlistに格納   ##########
def friend_name(friends_info_list):

    friends_name_list = []
    for friend_info in friends_info_list:
        friends_name_list.append(friend_info.name)

    return friends_name_list


##########   フォローしている人達のscreen_nameをlistに格納   ##########
def friend_screen_name(friends_info_list):

    friends_screen_name_list = []
    for friend_info in friends_info_list:
        friends_screen_name_list.append(friend_info.screen_name)

    return friends_screen_name_list


##########   フォローしている人達のidをlistに格納   ##########
def friend_ids(my_screen_name, my_self_info):

    friends_ids = tweepy.Cursor(
        api.friends_ids, id=my_screen_name, cursor=-1).items()
    friends_ids_list = []
    for friend_id in friends_ids:
        friends_ids_list.append(friend_id)

    # フォローしている人達のid_listに自分のidを追加する
    friends_ids_list.append(my_self_info.id)

    return friends_ids_list


##########   フォローしている人達のフォロー数をlistに格納   ##########
def friend_friends_count(friends_info_list):

    friends_friends_count_list = []
    for friend_info in friends_info_list:
        friends_friends_count_list.append(friend_info.friends_count)

    return friends_friends_count_list


##########   フォローしている人達のフォロワー数をlistに格納   ##########
def friend_followers_count(friends_info_list):

    friends_followers_count_list = []
    for friend_info in friends_info_list:
        friends_followers_count_list.append(friend_info.followers_count)

    return friends_followers_count_list


##########   フォローしている人達のフォロワー数/フォロー数の比率をlistに格納   ##########
def friend_ratio(my_self_info, friends_info_list):

    friends_followers_count_list = friend_followers_count(friends_info_list)
    friends_friends_count_list = friend_friends_count(friends_info_list)

    try:
        friend_ratio_list = []
        for i in range(my_self_info.friends_count + 1):
            ratio = round(
                friends_followers_count_list[i]/friends_friends_count_list[i], 2)
            friend_ratio_list.append(ratio)

    except ZeroDivisionError:
        friend_ratio_list = []
        for i in range(my_self_info.friends_count + 1):
            ratio = round(
                (friends_followers_count_list[i]+1)/(friends_friends_count_list[i]+1), 2)
            friend_ratio_list.append(ratio)

    finally:
        return friend_ratio_list


##########   フォローしている人達のツイート数をlistに格納   ##########
def friend_statuses_count(friends_info_list):

    friends_statuses_count_list = []
    for friend_info in friends_info_list:
        friends_statuses_count_list.append(friend_info.statuses_count)

    return friends_statuses_count_list


##########   フォローしている人達のアカウント作成日時をlistに格納   ##########
def friend_created_at(friends_info_list):

    friends_created_at_list = []
    for friend_info in friends_info_list:
        friends_created_at_list.append(friend_info.created_at)

    return friends_created_at_list


##########   フォローしている人達のプロフィール詳細文をlistに格納   ##########
def friend_description(friends_info_list):

    friends_description_list = []
    for friend_info in friends_info_list:
        friends_description_list.append(friend_info.description)

    return friends_description_list


##########   フォローしている人達のいいね数をlistに格納   ##########
def friend_favourites_count(friends_info_list):

    friends_favourites_count_list = []
    for friend_info in friends_info_list:
        friends_favourites_count_list.append(friend_info.favourites_count)

    return friends_favourites_count_list


####################################     フォロワーの情報取得     #########################################

##########   フォロワーの情報をlistに格納   ##########
def followers_info(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_info_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_info_list.append(follower)

    return followers_info_list

##########   フォロワーのiconをlistに格納   ##########


def follower_icon(followers_info_list):

    followers_icon_list = []
    for follower_info in followers_info_list:
        followers_icon_list.append(follower_info.profile_image_url_https)

    return followers_icon_list


##########   フォロワーのnameをlistに格納   ##########
def follower_name(followers_info_list):

    followers_name_list = []
    for follower_info in followers_info_list:
        followers_name_list.append(follower_info.name)

    return followers_name_list


##########   フォロワーのscreen_nameをlistに格納   ##########
def follower_screen_name(followers_info_list):

    followers_screen_name_list = []
    for follower_info in followers_info_list:
        followers_screen_name_list.append(follower_info.screen_name)

    return followers_screen_name_list


##########   フォロワーのidをlistに格納   ##########
def follower_ids(my_screen_name, my_self_info):

    followers_ids = tweepy.Cursor(
        api.followers_ids, id=my_screen_name, cursor=-1).items()
    followers_ids_list = []
    for follower_id in followers_ids:
        followers_ids_list.append(follower_id)

    # フォロワーのid_listに自分のidを追加する
    followers_ids_list.append(my_self_info.id)

    return followers_ids_list


##########   フォロワーのフォロー数をlistに格納   ##########
def follower_friends_count(followers_info_list):

    followers_friends_count_list = []
    for follower_info in followers_info_list:
        followers_friends_count_list.append(follower_info.friends_count)

    return followers_friends_count_list


##########   フォロワーのフォロワー数をlistに格納   ##########
def follower_followers_count(followers_info_list):

    followers_followers_count_list = []
    for follower_info in followers_info_list:
        followers_followers_count_list.append(follower_info.followers_count)

    return followers_followers_count_list


##########   フォロワーのフォロワー数/フォロー数の比率をlistに格納   ##########
def follower_ratio(my_self_info, followers_info_list):

    followers_followers_count_list = follower_followers_count(
        followers_info_list)
    followers_friends_count_list = follower_friends_count(followers_info_list)

    try:
        follower_ratio_list = []
        for i in range(my_self_info.followers_count + 1):
            ratio = round(
                followers_followers_count_list[i]/followers_friends_count_list[i], 2)
            follower_ratio_list.append(ratio)

    except ZeroDivisionError:
        follower_ratio_list = []
        for i in range(my_self_info.followers_count + 1):
            ratio = round(
                (followers_followers_count_list[i]+1)/(followers_friends_count_list[i]+1), 2)
            follower_ratio_list.append(ratio)

    finally:
        return follower_ratio_list


##########   フォロワーのツイート数をlistに格納   ##########
def follower_statuses_count(followers_info_list):

    followers_statuses_count_list = []
    for follower_info in followers_info_list:
        followers_statuses_count_list.append(follower_info.statuses_count)

    return followers_statuses_count_list


##########   フォロワーのアカウント作成日時をlistに格納   ##########
def follower_created_at(followers_info_list):

    followers_created_at_list = []
    for follower_info in followers_info_list:
        followers_created_at_list.append(follower_info.created_at)

    return followers_created_at_list


##########   フォロワーのプロフィール詳細文をlistに格納   ##########
def follower_description(followers_info_list):

    followers_description_list = []
    for follower_info in followers_info_list:
        followers_description_list.append(follower_info.description)

    return followers_description_list


##########   フォロワーのいいね数をlistに格納   ##########
def follower_favourites_count(followers_info_list):

    followers_favourites_count_list = []
    for follower_info in followers_info_list:
        followers_favourites_count_list.append(follower_info.favourites_count)

    return followers_favourites_count_list
