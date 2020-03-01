from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm
import tweepy
from .api_key import *


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


params = {
    "screen_name": "",
    "form": HelloForm(),

    "user_friends": "",
    "user_followers": "",
    "friends_ids_list": [],
    "friends_screen_name_list": [],
    "followers_ids_list": [],
    "followers_screen_name_list": [],
    "friend_followers_list": [],
    "friend_friends_list": [],
    "follower_followers_list": [],
    "follower_friends_list": [],
    "friend_friends_dict_sort": [],
    "rank_friend_friends": 0,
    "friend_followers_dict_sort": [],
    "rank_friend_followers": 0,
    "friend_dict": {},
    "friend_ratio_dict_sort": [],
    "rank_friend_ratio" : 0,

}

# def index(request):
#     if (request.method == "POST"):
#         params["screen_name"] = request.POST["screen_name"]
#         params["form"] = HelloForm(request.POST)

#         return render(request, "app/select.html", params)
#     else:
#         return render(request, "app/index.html", params)


# class HelloView(TemplateView):

#     def __init__(self):
#         self.params = {
#             "screen_name": "",
#             "form": HelloForm(),

#             "user_friends": "",
#             "user_followers": "",
#             "friends_ids_list": [],
#             "friends_screen_name_list": [],
#             "followers_ids_list": [],
#             "followers_screen_name_list": [],
#             "friend_followers_list": [],
#             "friend_friends_list": [],
#             "follower_followers_list": [],
#             "follower_friends_list": [],
#             "friend_friends_dict_sort": [],
#             "rank_friend_friends": 0,
#             "friend_followers_dict_sort": [],
#             "rank_friend_followers": 0,

#         }

#     def get(self, request):
#         return render(request, "app/index.html", self.params)

#     def post(self, request):
#         self.params["screen_name"] = request.POST["screen_name"]
#         self.params["form"] = HelloForm(request.POST)

#         return render(request, "app/select.html", self.params)

def info_get(request):
    if (request.method == "POST"):
        params["screen_name"] = request.POST["screen_name"]
        params["form"] = HelloForm(request.POST)

        user = api.get_user(screen_name=params["screen_name"])
        params["user_friends"] = user.friends_count
        params["user_followers"] = user.followers_count

        user_friends = params["user_friends"]
        user_followers = params["user_followers"]
        my_screen_name = params["screen_name"]

        ############    フォローのユーザーID/スクリーンネームの取得   ################

        # フォローのユーザーIDをリストに格納
        friends_ids = tweepy.Cursor(
            api.friends_ids, id=my_screen_name, cursor=-1).items()
        friends_ids_list = []
        for friend_id in friends_ids:
            friends_ids_list.append(friend_id)

        params["friends_ids_list"] = friends_ids_list

        # フォローのユーザースクリーンネームをリストに格納
        friends_screen_name_list = []
        for friend_id in friends_ids_list:
            friend = api.get_user(id=friend_id)
            friends_screen_name_list.append(friend.screen_name)

        # フォローしている人のスクリーンネームリストに自分のスクリーンネームを追加する
        friends_screen_name_list.append(my_screen_name)

        params["friends_screen_name_list"] = friends_screen_name_list

        ###########   フォロワーのユーザーID/スクリーンネームの取得    ################

        # フォロワーのユーザーIDをリストに格納
        followers_ids = tweepy.Cursor(
            api.followers_ids, id=my_screen_name, cursor=-1).items()
        followers_ids_list = []
        for follower_id in followers_ids:
            followers_ids_list.append(follower_id)

        params["followers_ids_list"] = followers_ids_list

        # フォロワーのユーザースクリーンネームをリストに格納
        followers_screen_name_list = []
        for follower_id in followers_ids_list:
            follower = api.get_user(id=follower_id)
            followers_screen_name_list.append(follower.screen_name)

        # フォローされている人のスクリーンネームリストに自分のスクリーンネームを追加する
        followers_screen_name_list.append(my_screen_name)

        params["followers_screen_name_list"] = followers_screen_name_list

        ############    各フォローのフォロワー数/フォロー数を取得   ################

        friend_followers_list = []
        friend_friends_list = []
        for friend_id in friends_ids_list:
            friend = api.get_user(id=friend_id)

            # フォローのフォロワー数/フォロー数をリストに格納
            friend_followers_list.append(friend.followers_count)
            friend_friends_list.append(friend.friends_count)

        params["friend_followers_list"] = friend_followers_list
        params["friend_friends_list"] = friend_friends_list

        ############    各フォロワーのフォロワー数/フォロー数を取得   ################

        follower_followers_list = []
        follower_friends_list = []
        for follower_id in followers_ids_list:
            follower = api.get_user(id=follower_id)

            # フォロワーのフォロワー数/フォロー数をリストに格納
            follower_followers_list.append(follower.followers_count)
            follower_friends_list.append(follower.friends_count)

        params["follower_followers_list"] = follower_followers_list
        params["follower_friends_list"] = follower_friends_list

        ############    フォローしている人達の各々のスクリーンネームとフォロー数/フォロワー数を辞書型に結びつける   ################

        # フォローしている人の各々のフォロー数/フォロワー数を二重リストに格納する
        friend_list = []
        friend_in_list = []

        for i in range(len(friend_friends_list)):
            friend_in_list.append(friend_friends_list[i])
            friend_in_list.append(friend_followers_list[i])
            friend_in_list
            friend_list.append(friend_in_list)
            friend_in_list = []

        # 自分のフォロー数/フォロワー数を二重リストに追加する
        friend_in_list.append(user_friends)
        friend_in_list.append(user_followers)
        friend_list.append(friend_in_list)

        # フォローしている人のスクリーンネームとフォロー数/フォロワー数を辞書方で格納する
        params["friend_dict"] = dict(zip(friends_screen_name_list, friend_list))

        return render(request, "app/select.html", params)

    else:
        return render(request, "app/index.html", params)


def rank_friend(request):

    friend_dict = params["friend_dict"]
    my_screen_name = params["screen_name"]

    ######     フォローしている人達でフォロー数が多い順で自分の順位を取得     ###########

    # フォローしている人のフォロー数が多い順にソート
    params["friend_friends_dict_sort"] = sorted(
        friend_dict.items(), key=lambda x: x[1][0], reverse=True)
    friend_friends_dict_sort = params["friend_friends_dict_sort"]

    # フォローしている人たちの中でフォロー数が多い順で自分の順位を計算
    rank_friend_friends = 0
    for screen_name in friend_friends_dict_sort:
        rank_friend_friends += 1
        if screen_name[0] == my_screen_name:
            break

    params["rank_friend_friends"] = rank_friend_friends

    return render(request, "app/rank_friend.html", params)



def rank_follower(request):

    friend_dict = params["friend_dict"]
    my_screen_name = params["screen_name"]

    ######     フォローしている人達でフォロワー数が多い順で自分の順位を取得     ###########

    # フォローしている人のフォロワー数が多い順にソート
    params["friend_followers_dict_sort"] = sorted(
        friend_dict.items(), key=lambda x: x[1][1], reverse=True)
    friend_followers_dict_sort = params["friend_followers_dict_sort"]

    # フォローしている人たちの中でフォロワー数が多い順で自分の順位を計算
    rank_friend_followers = 0
    for screen_name in friend_followers_dict_sort:
        rank_friend_followers += 1
        if screen_name[0] == my_screen_name:
            break

    params["rank_friend_followers"] = rank_friend_followers

    return render(request, "app/rank_follower.html", params)


def rank_ratio(request):

    my_screen_name = params["screen_name"]
    friend_friends_list = params["friend_friends_list"]
    friend_followers_list = params["friend_followers_list"]
    user_friends = params["user_friends"]
    user_followers = params["user_followers"]
    friends_screen_name_list = params["friends_screen_name_list"]

    ############    フォローしている人達の各々のスクリーンネームとフォロワー数/フォロー数の比率を辞書型に結びつける   ################


    #フォロワー数/フォロー数の比率をリストに格納する
    friend_ratio_list = []
    for i in range(len(friend_friends_list)):
        ratio = round(friend_followers_list[i]/friend_friends_list[i], 2)
        friend_ratio_list.append(ratio)

    user_ratio = round(user_followers/user_friends, 2)
    friend_ratio_list.append(user_ratio)

    #フォローしている人のスクリーンネームとフォロワー数/フォロー数の比率を辞書方で格納する
    friend_ratio_dict = dict(zip(friends_screen_name_list, friend_ratio_list ))


    ######     フォローしている人達でフォロワー数/フォロー数の比率が高い順で自分の順位を取得     ###########


    #フォローしている人のフォロワー数/フォロー数の比率が高い順にソート
    params["friend_ratio_dict_sort"] = sorted(friend_ratio_dict.items(), key=lambda x: x[1], reverse=True)
    friend_ratio_dict_sort = params["friend_ratio_dict_sort"]

    #フォローしている人たちの中でフォロワー数が多い順で自分の順位を計算
    rank_friend_ratio = 0
    for screen_name in friend_ratio_dict_sort:
        rank_friend_ratio += 1
        if screen_name[0] == my_screen_name:
            break

    params["rank_friend_ratio"] = rank_friend_ratio

    return render(request, "app/rank_ratio.html", params)