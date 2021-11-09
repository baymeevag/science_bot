from utils.auth import oauth
from utils.config import TERMS

if __name__ == '__main__':
    api = oauth()
    tweets = {}
    
    for term in TERMS:
        response = api.search_tweets(term)
        tweets[term] = [item._json for item in response]
    tweet_ids = [[item['id'] for item in v] for k, v in tweets.items()]
    tweet_ids_flat = [item for sublist in tweet_ids for item in sublist]

    for tweet_id in tweet_ids_flat:
        try:
            api.create_favorite(tweet_id)
        except:
            continue