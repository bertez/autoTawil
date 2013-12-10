#!/usr/bin/env python

import schedule
import time
import tweepy

from crawler import TweetCrawler
from generator import TweetGenerator

from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

c = TweetCrawler('Tawil', 'data/tweets.db', 5000)
t = TweetGenerator('data/tweets.db', 10)
t.update_database()


def crawl():
    print('Crawling')
    c.crawl()
    print('Updating database')
    t.update_database()


def tweet():
    text = t.generate()

    print('Tweeting:')
    print text

    try:
        api.update_status(text)
    except tweepy.TweepError as e:
        print e


schedule.every(10).minutes.do(tweet)
schedule.every().hour.do(crawl)

while True:
    schedule.run_pending()
    time.sleep(1)
