#!/usr/bin/env python
"""This module crawls and stores tweets from a single user"""

import tweepy
import time
import pickle

from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweet_list = []
i = None

while True:
    print '---- Storage length: {0} // Last id: {1}'.format(len(tweet_list), i)
    print
    for result in api.user_timeline(screen_name='Tawil', count=100, max_id=i,
                                    include_rts=False, exclude_replies=True):
        i = result.id - 1

        tweet = {}

        tweet['id'] = result.id
        tweet['text'] = result.text

        print result.text

        tweet_list.append(tweet)

    if len(tweet_list) >= 100:
        break

    time.sleep(5)

print
print 'Saving data...'
data_export = open('data/tweets.db', 'w')

pickle.dump(tweet_list, data_export)

print 'Done.'
