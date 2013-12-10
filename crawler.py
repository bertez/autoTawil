#!/usr/bin/env python
"""This module crawls and stores tweets from a single user."""

import tweepy
import time
import pickle
import helpers

from config import *


class TweetCrawler(object):
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
            self.since_id = None

    def crawl(self):
        i = None

        while True:
            if self.since_id:
                request = self.api.user_timeline(screen_name=self.user,
                                                 count=200,
                                                 since_id=self.since_id,
                                                 max_id=i, include_rts=False,
                                                 exclude_replies=True)
            else:
                request = self.api.user_timeline(screen_name=self.user,
                                                 count=200,
                                                 max_id=i, include_rts=False,
                                                 exclude_replies=True)

            if len(request) == 0:
                break

            for result in request:
                i = result.id - 1

                tweet = {}

                tweet['id'] = result.id
                tweet['text'] = helpers.processTweet(result.text)

                print tweet['text']

                self.tweet_list.append(tweet)

            time.sleep(5)

        self.save()

    def save(self):
        sorted_list = sorted(self.tweet_list, key=lambda k: k['id'],
                             reverse=True)
        data_export = open(self.storage_file, 'w')

        pickle.dump(sorted_list[:self.max_tweets], data_export)
        print 'Saved.'


def main():
    crawler = TweetCrawler('Tawil', 'data/tweets.db', 5000)
    crawler.crawl()

if __name__ == '__main__':
    main()
