from random import randint, choice
import tweepy
import time
import webbrowser
import re
import sys
sys.path.append('.')
sys.path.append('..')
from utils.auth import oauth

class MarkovBot:
    def __init__(self, tweets_a_day): # path to corpus
        self.sleep_timer = int(60 * 60 * tweets_a_day)
        self.transition = {}
        self.start_words = []
        self.api = oauth()
        self.init_corpus(path_to_corpus)
        
    def init_corpus(self, path_to_corpus):
        with open(path_to_corpus, 'r') as f:
            for line in f.readlines():
                words = line.split()
                self.start_words.append(words[0])
                n = len(words)
                for word1, word2 in zip(words[:(n - 1)], words[1:]):
                    if word1 in self.transition:
                        self.transition[word1].append(word2)
                    else:
                        self.transition[word1] = [word2]
                        
    def generate(self):
        current_word = choice(self.start_words)
        result = [current_word]
        while current_word in self.transition.keys() and self.transition[current_word]:
            current_word = choice(self.transition[current_word])
            result.append(current_word)
        return ' '.join(result)
    
    def get_tweet(self):
        tweet = self.generate()
        while len(tweet.decode('utf8')) > 140 or len(tweet.split()) < 7:
            tweet = self.generate()
        return tweet
        
    def run(self):
        while True:
            tweet = self.get_tweet()
            self.api.update_status(tweet) # Posts to twitter
            time.sleep(self.sleep_timer)