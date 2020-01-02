import re
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

takeout_dir = os.getcwd()+'\\Takeout'
search_file = takeout_dir+'\\YouTube\\history\\search-history.html'
watch_file = takeout_dir+'\\YouTube\\history\\watch-history.html'
comments_file = takeout_dir+'\\YouTube\\my-comments\\my-comments.html'
live_comments_file = takeout_dir+'\\YouTube\\my-live-chat-messages\\my-live-chat-messages.html'
likes_file = takeout_dir+'\\YouTube\\playlists\\likes.json'
subscriptions_file = takeout_dir+'\\YouTube\\subscriptions\\subscriptions.json'


class get_data():
    def __init__(self):
        self.search_text = None
        self.watch_metrics = None
        self.comments_metrics = None
        self.total_likes = None
        self.total_subscriptions = None

    def search_data(self):
        with open(search_file, 'r', encoding='utf-8') as sf:
            search_history = BeautifulSoup(sf,'lxml')
        searches = search_history.find_all('a')
        self.search_text = [search.contents[0] for search in searches]


    def watch_data(self):
        with open(watch_file, 'r', encoding='utf-8') as wf:
            watch_history = BeautifulSoup(wf, 'lxml')

        self.watch_metrics = {
            'channels': watch_history.find_all(href=re.compile("channel")),
            'videos': watch_history.find_all(href=re.compile("watch")),
            'timestamps': watch_history.find_all(string=re.compile("UTC")),
        }

        for i in range(len(self.watch_metrics['timestamps'])):
            self.watch_metrics['timestamps'][i] = datetime.strptime(self.watch_metrics['timestamps'][i][:-4], "%b %d, %Y, %I:%M:%S %p")



    def comments_data(self):
        with open(comments_file, 'r') as cf:
            comments_history = BeautifulSoup(cf, 'lxml')
        with open(live_comments_file, 'r') as lcf:
            live_comments_history = BeautifulSoup(lcf, 'lxml')
        #comments = comments_history.find_all('a')
        #comments.append(live_comments_history.find_all('a'))

        comment_time = comments_history.find_all(string=re.compile("UTC"))
        comment_time.extend(live_comments_history.find_all(string=re.compile("UTC")))

        self.comments_metrics = {
            'no_of_comments': len(comments_history.find_all("li"))+len(live_comments_history.find_all("li")),
            'comment_time': comment_time
        }

        print()


    def like_data(self):
        with open(likes_file, 'r', encoding='utf-8') as lf:
            like_history = json.load(lf)
        self.total_likes = len(like_history)

    def subscriptions_data(self):
        with open(subscriptions_file, 'r', encoding='utf-8') as sf:
            subscriptions_history = json.load(sf)
        self.total_subscriptions = len(subscriptions_history)


if __name__ == "__main__":
    x = get_data()
    x.subscriptions_data()
    print(x.total_subscriptions)
