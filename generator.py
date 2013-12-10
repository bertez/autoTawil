#!/usr/bin/env python
"""This module uses a simple Markov Chain algorithm to generate random tweets
using the crawled tweets archive as seed."""

import pickle
from collections import defaultdict
from random import random
from random import choice
import tweepy

from config import *


class TweetGenerator(object):
    def __init__(self, archive, samples):

        self.tweets = pickle.load(open(archive))
        self.samples = samples

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        self.titles = []

        for tweet in self.tweets:
            self.titles.append(tweet['text'])

        self.markov_map = defaultdict(lambda: defaultdict(int))

        self.lookback = 2

        #Generate map in the form word1 -> word2 -> occurences of word2 after word1
        for title in self.titles:
            title = title.split()
            if len(title) > self.lookback:
                for i in xrange(len(title) + 1):
                    self.markov_map[' '.join(title[max(0, i - self.lookback):i])][' '.join(title[i:i + 1])] += 1

        #Convert map to the word1 -> word2 -> probability of word2 after word1
        for word, following in self.markov_map.items():
            total = float(sum(following.values()))
            for key in following:
                following[key] /= total

    def sample(self, items):
        next_word = None
        t = 0.0
        for k, v in items:
            t += v
            if t and random() < v / t:
                next_word = k
        return next_word

    def generate(self):
        sentences = []
        while len(sentences) < self.samples:
            sentence = []
            next_word = self.sample(self.markov_map[''].items())
            while next_word != '':
                sentence.append(next_word)
                next_word = self.sample(self.markov_map[' '.join(sentence[-self.lookback:])].items())
            sentence = ' '.join(sentence)
            flag = True

            #Prune titles that are substrings of actual titles
            for title in self.titles:
                if sentence in title:
                    flag = False
                    break
            if flag:
                sentences.append(sentence)

        return choice(sentences)

    def send_tweet(self):
        try:
            self.api.update_status(self.generate())
        except tweepy.TweepError as e:
            print e


def main():
    crawler = TweetGenerator('data/tweets.db', 10)
    crawler.send_tweet()

if __name__ == '__main__':
    main()
