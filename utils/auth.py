import tweepy
from decouple import config

def oauth():
    auth = tweepy.OAuthHandler(
        config('TWITTER_CONSUMER_KEY'),
        config('TWITTER_CONSUMER_SECRET')
        )
    auth.set_access_token(
        config('TWITTER_ACCESS_KEY'), 
        config('TWITTER_ACCESS_SECRET'))

    return tweepy.API(auth)