#!/usr/bin/env python
"""This module crawls and stores tweets from a single user."""

import tweepy
import time
import pickle

from config import *


class TweetsCrawler(object):
    def __init__(self, user, storage_file, max_tweets):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        self.user = user
        self.storage_file = storage_file
        self.max_tweets = max_tweets

        try:
            current_tweets = pickle.load(open(storage_file))
        except IOError:
            current_tweets = []

        if(len(current_tweets) > 0):
            self.tweet_list = current_tweets
            self.since_id = current_tweets[0]['id']
        else:
            self.tweet_list = []

        print len(self.tweet_list)

    def crawl(self):
        i = None

        while True:
            request = self.api.user_timeline(screen_name=self.user,
                                             count=100,
                                             max_id=i, include_rts=False,
                                             exclude_replies=True)
            for result in request:
                i = result.id - 1

                tweet = {}

                tweet['id'] = result.id
                tweet['text'] = result.text

                print result.text

                self.tweet_list.append(tweet)

            if len(self.tweet_list) >= self.max_tweets:
                break

            time.sleep(5)

        self.save()

    def save(self):
        #ensure only max_tweets are stored
        data_export = open(self.storage_file, 'w')
        pickle.dump(self.tweet_list, data_export)
        print 'Saved.'


def main():
    crawler = TweetsCrawler('Tawil', 'data/tweets.db', 100)
    crawler.crawl()

if __name__ == '__main__':
    main()
