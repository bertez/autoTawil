#autoTawil

This is a set of python modules that work together to crawl tweets from a Twitter user and then generate random tweets using a simple [Markov algorithm](http://en.wikipedia.org/wiki/Markov_chain). It also has a queue script to automate the process of crawling/generating/posting.

It was created by [@bertez](https://twitter.com/bertez) as a joke for [@Tawil](https://twitter.com/Tawil) but the code is quite simple and can be easily adapted to any other user.

It uses the [Tweepy](https://github.com/tweepy/tweepy/) and [Schedule](https://github.com/dbader/schedule) Python libraries. 

Also, to build this I have refactored some code from: <https://gist.github.com/grantslatton/7694811>. So Thank you :)

*Note: the code actually has a few known non critical bugs but it works just fine for its main purpose: build a simple funny Twitter bot.*
