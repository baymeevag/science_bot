import sys
from MarkovBot import MarkovBot

if __name__ == '__main__':
    topic = sys.argv[1]

    bot = MarkovBot(topic)

    tweet = bot.get_tweet()

    bot.api.update_status(tweet)