from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm
import tweepy
from .api_key import *


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)

class HelloView(TemplateView):

    def __init__(self):
        self.params = {
            "screen_name" : "",
            "form" : HelloForm(),

            "user_friends" : "",
            "user_followers" : "",
            "friends_ids_list" : [],
            "friends_screen_name_list" : [],
            "followers_ids_list" : [],
            "followers_screen_name_list": [],
            "friend_followers_list" : [],
            "friend_friends_list" : [],
            "follower_followers_list" : [],
            "follower_friends_list" : [],
            "friend_friends_dict_sort" : [],
            "rank_friend_friends" : 0,
            "friend_followers_dict_sort" : [],
            "rank_friend_followers" : 0,

        }

    def get(self, request):
        return render(request, "app/index.html", self.params)

    def post(self, request):
        self.params["screen_name"] = request.POST["screen_name"]
        self.params["form"] = HelloForm(request.POST)
        
        user = api.get_user(screen_name = self.params["screen_name"])
        self.params["user_friends"] = user.friends_count
        self.params["user_followers"] = user.followers_count

        user_friends = self.params["user_friends"]
        user_followers = self.params["user_followers"]
        my_screen_name = self.params["screen_name"]


        ############    フォローのユーザーID/スクリーンネームの取得   ################

        #フォローのユーザーIDをリストに格納
        friends_ids = tweepy.Cursor(api.friends_ids, id = my_screen_name, cursor = -1).items()
        friends_ids_list = []
        for friend_id in friends_ids:
            friends_ids_list.append(friend_id)

        self.params["friends_ids_list"] = friends_ids_list
            
        #フォローのユーザースクリーンネームをリストに格納
        friends_screen_name_list = []
        for friend_id in friends_ids_list:
            friend = api.get_user(id = friend_id)
            friends_screen_name_list.append(friend.screen_name)

        #フォローしている人のスクリーンネームリストに自分のスクリーンネームを追加する
        friends_screen_name_list.append(my_screen_name)

        self.params["friends_screen_name_list"] = friends_screen_name_list


        ###########   フォロワーのユーザーID/スクリーンネームの取得    ################

        #フォロワーのユーザーIDをリストに格納
        followers_ids = tweepy.Cursor(api.followers_ids, id = my_screen_name, cursor = -1).items()
        followers_ids_list = []
        for follower_id in followers_ids:
            followers_ids_list.append(follower_id)
        
        self.params["followers_ids_list"] = followers_ids_list

        #フォロワーのユーザースクリーンネームをリストに格納
        followers_screen_name_list = []
        for follower_id in followers_ids_list:
            follower = api.get_user(id = follower_id)
            followers_screen_name_list.append(follower.screen_name)

        #フォローされている人のスクリーンネームリストに自分のスクリーンネームを追加する
        followers_screen_name_list.append(my_screen_name)

        self.params["followers_screen_name_list"] = followers_screen_name_list



        ############    各フォローのフォロワー数/フォロー数を取得   ################

        friend_followers_list = []
        friend_friends_list = []
        for friend_id in friends_ids_list:
            friend = api.get_user(id = friend_id)

            #フォローのフォロワー数/フォロー数をリストに格納
            friend_followers_list.append(friend.followers_count)
            friend_friends_list.append(friend.friends_count)

        self.params["friend_followers_list"] = friend_followers_list
        self.params["friend_friends_list"] = friend_friends_list


        ############    各フォロワーのフォロワー数/フォロー数を取得   ################

        follower_followers_list = []
        follower_friends_list = []
        for follower_id in followers_ids_list:
            follower = api.get_user(id = follower_id) 

            #フォロワーのフォロワー数/フォロー数をリストに格納
            follower_followers_list.append(follower.followers_count)
            follower_friends_list.append(follower.friends_count)

        self.params["follower_followers_list"] = follower_followers_list
        self.params["follower_friends_list"] = follower_friends_list

        

        ############    フォローしている人達の各々のスクリーンネームとフォロー数/フォロワー数を辞書型に結びつける   ################

        #フォローしている人の各々のフォロー数/フォロワー数を二重リストに格納する
        friend_list = []
        friend_in_list = []

        for i in range(len(friend_friends_list)):
            friend_in_list.append(friend_friends_list[i])
            friend_in_list.append(friend_followers_list[i])
            friend_in_list
            friend_list.append(friend_in_list)
            friend_in_list = []

        #自分のフォロー数/フォロワー数を二重リストに追加する
        friend_in_list.append(user_friends)
        friend_in_list.append(user_followers)
        friend_list.append(friend_in_list)

        #フォローしている人のスクリーンネームとフォロー数/フォロワー数を辞書方で格納する
        friend_dict = dict(zip(friends_screen_name_list, friend_list ))





        ######     フォローしている人達でフォロー数が多い順で自分の順位を取得     ###########

        #フォローしている人のフォロー数が多い順にソート
        self.params["friend_friends_dict_sort"] = sorted(friend_dict.items(), key=lambda x:x[1][0], reverse=True)
        friend_friends_dict_sort = self.params["friend_friends_dict_sort"]

        #フォローしている人たちの中でフォロー数が多い順で自分の順位を計算
        rank_friend_friends = 0
        for screen_name in friend_friends_dict_sort:
            rank_friend_friends += 1
            if screen_name[0] == my_screen_name:
                break

        self.params["rank_friend_friends"] = rank_friend_friends

        ######     フォローしている人達でフォロワー数が多い順で自分の順位を取得     ###########


        #フォローしている人のフォロワー数が多い順にソート
        self.params["friend_followers_dict_sort"] = sorted(friend_dict.items(), key=lambda x:x[1][1], reverse=True)
        friend_followers_dict_sort = self.params["friend_followers_dict_sort"]

        #フォローしている人たちの中でフォロワー数が多い順で自分の順位を計算
        rank_friend_followers = 0
        for screen_name in friend_followers_dict_sort:
            rank_friend_followers += 1
            if screen_name[0] == my_screen_name:
                break
        
        self.params["rank_friend_followers"] = rank_friend_followers

        return render(request, "app/rank.html", self.params)
       








