#!/usr/bin/env python

import schedule
import time

from crawler import TweetCrawler
from generator import TweetGenerator

c = TweetCrawler('Tawil', 'data/tweets.db', 5000)
t = TweetGenerator('data/tweets.db', 10)

def crawl():
    print('Crawling')
    c.crawl()

def tweet():
    print('Tweeting')
    t.send_tweet()


schedule.every(1).minutes.do(tweet)
schedule.every().hour.do(crawl)

while True:
    schedule.run_pending()
    time.sleep(1)
