from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm
import tweepy
from .api_key import *
from .models import Friend_Info, Follower_Info


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


params = {
    "my_self_info" : "",
    "screen_name": "",
    "form": HelloForm(),
    "friend": "",
    "follower": "",
    "rank" : 0,
}

def friend_friend_rank_asc(request):
    params["friend"] = params["friend"].order_by("friends_count")
    friend_rank()
    return render(request, "app/friend.html", params)

def friend_friend_rank_desc(request):
    params["friend"] = params["friend"].order_by("friends_count").reverse()
    friend_rank()
    return render(request, "app/friend.html", params)

def friend_follower_rank_asc(request):
    params["friend"] = params["friend"].order_by("followers_count")
    friend_rank()
    return render(request, "app/friend.html", params)

def friend_follower_rank_desc(request):
    params["friend"] = params["friend"].order_by("followers_count").reverse()
    friend_rank()
    return render(request, "app/friend.html", params)

def friend_ratio_rank_asc(request):
    params["friend"] = params["friend"].order_by("ratio")
    friend_rank()
    return render(request, "app/friend.html", params)

def friend_ratio_rank_desc(request):
    params["friend"] = params["friend"].order_by("ratio").reverse()
    friend_rank()
    return render(request, "app/friend.html", params)

def follower_friend_rank_asc(request):
    params["follower"] = params["follower"].order_by("friends_count")
    follower_rank()
    return render(request, "app/follower.html", params)

def follower_friend_rank_desc(request):
    params["follower"] = params["follower"].order_by("friends_count").reverse()
    follower_rank()
    return render(request, "app/follower.html", params)

def follower_follower_rank_asc(request):
    params["follower"] = params["follower"].order_by("followers_count")
    follower_rank()
    return render(request, "app/follower.html", params)

def follower_follower_rank_desc(request):
    params["follower"] = params["follower"].order_by("followers_count").reverse()
    follower_rank()
    return render(request, "app/follower.html", params)

def follower_ratio_rank_asc(request):
    params["follower"] = params["follower"].order_by("ratio")
    follower_rank()
    return render(request, "app/follower.html", params)

def follower_ratio_rank_desc(request):
    params["follower"] = params["follower"].order_by("ratio").reverse()
    follower_rank()
    return render(request, "app/follower.html", params)


def friend_rank():
    params["rank"] = 0
    for screen_name in params["friend"]:
        params["rank"] += 1
        if screen_name.screen_name == params["screen_name"]:
            break
    return params["rank"]

def follower_rank():
    params["rank"] = 0
    for screen_name in params["follower"]:
        params["rank"] += 1
        if screen_name.screen_name == params["screen_name"]:
            break
    return params["rank"]


def select_friend(request):
    return render(request, "app/select_friend.html")

def select_follower(request):
    return render(request, "app/select_follower.html")


####################################     フォローしている人/フォロワーの全情報をDBに格納     #########################################

def info_get(request):

    if (request.method == "POST"):

        params["screen_name"] = request.POST["screen_name"]
        params["form"] = HelloForm(request.POST)

        my_screen_name = params["screen_name"]
        my_self_info = api.get_user(screen_name=params["screen_name"])
        params["my_self_info"] = my_self_info

        # fridnd_info_get(my_screen_name, my_self_info)
        # follower_info_get(my_screen_name, my_self_info)

        params["friend"] = Friend_Info.objects.filter(my_screen_name=my_screen_name)
        params["follower"] = Follower_Info.objects.filter(my_screen_name=my_screen_name)

        return render(request, "app/select.html", params)

    else:
        return render(request, "app/index.html", params)





####################################     フォローしている人の情報をDBに格納     #########################################

def fridnd_info_get(my_screen_name, my_self_info):

    ############          フォローしている人の情報をlistにして取得          ###################
    friends_icon_list = friend_icon(my_screen_name, my_self_info)
    friends_name_list = friend_name(my_screen_name, my_self_info)
    friends_screen_name_list = friend_screen_name(my_screen_name, my_self_info)
    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_friends_count_list = friend_friends_count(my_screen_name, my_self_info)
    friends_followers_count_list = friend_followers_count(my_screen_name, my_self_info)
    friends_ratio_list = friend_ratio(my_screen_name, my_self_info)
    # friends_statuses_count_list = friend_statuses_count(my_screen_name, my_self_info)
    # friends_created_at_list = friend_created_at(my_screen_name, my_self_info)
    # friends_description_list = friend_description(my_screen_name, my_self_info)
    # friends_favourites_count_list = friend_favourites_count(my_screen_name, my_self_info)

    #前のデータを全消去する
    Friend_Info.objects.filter(my_screen_name=params["screen_name"]).delete()

    for i in range(my_self_info.friends_count + 1):
            
        friend_info = Friend_Info(
            my_screen_name = my_screen_name,
            profile_image_url_https = friends_icon_list[i],
            name = friends_name_list[i],
            screen_name = friends_screen_name_list[i],
            user_id = friends_ids_list[i],
            friends_count = friends_friends_count_list[i],
            followers_count = friends_followers_count_list[i],
            ratio = friends_ratio_list[i],
            statuses_count = 0,#friends_statuses_count_list[i],
            created_at = "2020-03-08",#friends_created_at_list[i],
            description = "NO",#friends_description_list[i],
            favourites_count = 0,#friends_favourites_count_list[i]
            )

        friend_info.save()
    
    params["friend"] = Friend_Info.objects.all()





####################################     フォロワーの情報をDBに格納     #########################################

def follower_info_get(my_screen_name, my_self_info):

    ############          フォロワーの情報をlistにして取得          ###################
    followers_icon_list = follower_icon(my_screen_name, my_self_info)
    followers_name_list = follower_name(my_screen_name, my_self_info)
    followers_screen_name_list = follower_screen_name(my_screen_name, my_self_info)
    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_friends_count_list = follower_friends_count(my_screen_name, my_self_info)
    followers_followers_count_list = follower_followers_count(my_screen_name, my_self_info)
    followers_ratio_list = follower_ratio(my_screen_name, my_self_info)
    # followers_statuses_count_list = follower_statuses_count(my_screen_name, my_self_info)
    # followers_created_at_list = follower_created_at(my_screen_name, my_self_info)
    # followers_description_list = follower_description(my_screen_name, my_self_info)
    # followers_favourites_count_list = follower_favourites_count(my_screen_name, my_self_info)
    
    #前のデータを全消去する
    Follower_Info.objects.filter(my_screen_name=params["screen_name"]).delete()

    for i in range(my_self_info.followers_count + 1):
            
        follower_info = Follower_Info(
            my_screen_name = my_screen_name,
            profile_image_url_https = followers_icon_list[i],
            name = followers_name_list[i],
            screen_name = followers_screen_name_list[i],
            user_id = followers_ids_list[i],
            friends_count = followers_friends_count_list[i],
            followers_count = followers_followers_count_list[i],
            ratio = followers_ratio_list[i],
            statuses_count = 0,#followers_statuses_count_list[i],
            created_at = "2020-03-08",#followers_created_at_list[i],
            description = "NO",#followers_description_list[i],
            favourites_count = 0,#followers_favourites_count_list[i]
            )

        follower_info.save()
    
    params["follower"] = Follower_Info.objects.all()



####################################     フォローしている人の情報取得     #########################################



##########   フォローしている人達のiconをlistに格納   ##########
def friend_icon(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_icon_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_icon_list.append(friend.profile_image_url_https)

    return friends_icon_list


##########   フォローしている人達のnameをlistに格納   ##########
def friend_name(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_name_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_name_list.append(friend.name)

    return friends_name_list


##########   フォローしている人達のscreen_nameをlistに格納   ##########
def friend_screen_name(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_screen_name_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_screen_name_list.append(friend.screen_name)

    return friends_screen_name_list



##########   フォローしている人達のidをlistに格納   ##########
def friend_ids(my_screen_name, my_self_info):

    friends_ids = tweepy.Cursor(api.friends_ids, id=my_screen_name, cursor=-1).items()
    friends_ids_list = []
    for friend_id in friends_ids:
        friends_ids_list.append(friend_id)

    # フォローしている人達のid_listに自分のidを追加する
    friends_ids_list.append(my_self_info.id)

    return friends_ids_list



##########   フォローしている人達のフォロー数をlistに格納   ##########
def friend_friends_count(my_screen_name, my_self_info):
    
    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_friends_count_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_friends_count_list.append(friend.friends_count)

    return friends_friends_count_list

        


##########   フォローしている人達のフォロワー数をlistに格納   ##########
def friend_followers_count(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_followers_count_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_followers_count_list.append(friend.followers_count)

    return friends_followers_count_list


##########   フォローしている人達のフォロワー数/フォロー数の比率をlistに格納   ##########
def friend_ratio(my_screen_name, my_self_info):

    friends_followers_count_list = friend_followers_count(my_screen_name, my_self_info)
    friends_friends_count_list = friend_friends_count(my_screen_name, my_self_info)

    try:
        friend_ratio_list = []
        for i in range(my_self_info.friends_count + 1):
            ratio = round(friends_followers_count_list[i]/friends_friends_count_list[i], 2)
            friend_ratio_list.append(ratio)
    
    except ZeroDivisionError:
        friend_ratio_list = []
        for i in range(my_self_info.friends_count + 1):
            ratio = round((friends_followers_count_list[i]+1)/(friends_friends_count_list[i]+1), 2)
            friend_ratio_list.append(ratio)

    finally:
        return friend_ratio_list
    


##########   フォローしている人達のツイート数をlistに格納   ##########
def friend_statuses_count(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_statuses_count_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_statuses_count_list.append(friend.statuses_count)

    return friends_statuses_count_list


##########   フォローしている人達のアカウント作成日時をlistに格納   ##########
def friend_created_at(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_created_at_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_created_at_list.append(friend.created_at)

    return friends_created_at_list


##########   フォローしている人達のプロフィール詳細文をlistに格納   ##########
def friend_description(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_description_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_description_list.append(friend.description)

    return friends_description_list


##########   フォローしている人達のいいね数をlistに格納   ##########
def friend_favourites_count(my_screen_name, my_self_info):

    friends_ids_list = friend_ids(my_screen_name, my_self_info)
    friends_favourites_count_list = []
    for friend_id in friends_ids_list:
        friend = api.get_user(id=friend_id)
        friends_favourites_count_list.append(friend.favourites_count)

    return friends_favourites_count_list




####################################     フォロワーの情報取得     #########################################



##########   フォロワーのiconをlistに格納   ##########
def follower_icon(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_icon_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_icon_list.append(follower.profile_image_url_https)

    return followers_icon_list


##########   フォロワーのnameをlistに格納   ##########
def follower_name(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_name_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_name_list.append(follower.name)

    return followers_name_list


##########   フォロワーのscreen_nameをlistに格納   ##########
def follower_screen_name(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_screen_name_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_screen_name_list.append(follower.screen_name)

    return followers_screen_name_list



##########   フォロワーのidをlistに格納   ##########
def follower_ids(my_screen_name, my_self_info):

    followers_ids = tweepy.Cursor(api.followers_ids, id=my_screen_name, cursor=-1).items()
    followers_ids_list = []
    for follower_id in followers_ids:
        followers_ids_list.append(follower_id)

    # フォロワーのid_listに自分のidを追加する
    followers_ids_list.append(my_self_info.id)

    return followers_ids_list



##########   フォロワーのフォロー数をlistに格納   ##########
def follower_friends_count(my_screen_name, my_self_info):
    
    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_friends_count_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_friends_count_list.append(follower.friends_count)

    return followers_friends_count_list

        


##########   フォロワーのフォロワー数をlistに格納   ##########
def follower_followers_count(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_followers_count_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_followers_count_list.append(follower.followers_count)

    return followers_followers_count_list


##########   フォロワーのフォロワー数/フォロー数の比率をlistに格納   ##########
def follower_ratio(my_screen_name, my_self_info):

    followers_followers_count_list = follower_followers_count(my_screen_name, my_self_info)
    followers_friends_count_list = follower_friends_count(my_screen_name, my_self_info)

    try:
        follower_ratio_list = []
        for i in range(my_self_info.followers_count + 1):
            ratio = round(followers_followers_count_list[i]/followers_friends_count_list[i], 2)
            follower_ratio_list.append(ratio)
    
    except ZeroDivisionError:
        follower_ratio_list = []
        for i in range(my_self_info.followers_count + 1):
            ratio = round((followers_followers_count_list[i]+1)/(followers_friends_count_list[i]+1), 2)
            follower_ratio_list.append(ratio)

    finally:
        return follower_ratio_list
    


##########   フォロワーのツイート数をlistに格納   ##########
def follower_statuses_count(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_statuses_count_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_statuses_count_list.append(follower.statuses_count)

    return followers_statuses_count_list


##########   フォロワーのアカウント作成日時をlistに格納   ##########
def follower_created_at(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_created_at_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_created_at_list.append(follower.created_at)

    return followers_created_at_list


##########   フォロワーのプロフィール詳細文をlistに格納   ##########
def follower_description(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_description_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_description_list.append(follower.description)

    return followers_description_list


##########   フォロワーのいいね数をlistに格納   ##########
def follower_favourites_count(my_screen_name, my_self_info):

    followers_ids_list = follower_ids(my_screen_name, my_self_info)
    followers_favourites_count_list = []
    for follower_id in followers_ids_list:
        follower = api.get_user(id=follower_id)
        followers_favourites_count_list.append(follower.favourites_count)

    return followers_favourites_count_list

