import re
import string


def processTweet(tweet):

    characters = set(string.punctuation)

    #urls
    tweet = re.sub(r'((www\.[\s]+)|(https?://[^\s]+))', '', tweet)

    #users
    tweet = re.sub(r'@[^\s]+', '', tweet)

    #hashtags
    #tweet = re.sub(r'#([^\s]+)', '', tweet)

    #punctuation
    #tweet = ''.join(ch for ch in tweet if ch not in characters)

    #extra whitespace
    tweet = ' '.join(tweet.split())

    #strip
    tweet = tweet.strip()

    return tweet
