from utils.auth import oauth
from utils.config import TOPIC
from generators.Markov import Markov

if __name__ == '__main__':
    api = oauth()
    bot = Markov(TOPIC)

    tweet = bot.get_tweet()
    api.update_status(tweet)
        