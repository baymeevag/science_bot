import tweepy
import os

def oauth():
    auth = tweepy.OAuthHandler(
        os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET']
        )
    auth.set_access_token(
        os.environ['TWITTER_ACCESS_KEY'], 
        os.environ['TWITTER_ACCESS_SECRET'])

    return tweepy.API(auth)