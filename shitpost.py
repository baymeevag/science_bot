import sys
from utils.auth import oauth
from generators.Markov import Markov

if __name__ == '__main__':
    topic = sys.argv[1]

    bot =  Markov(topic)

    tweet = bot.get_tweet()

    api = oauth()

    api.update_status(tweet)