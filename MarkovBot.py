from random import randint, choice
import tweepy
import time
import pandas as pd
import re
import os
import sys
from utils.auth import oauth
from CorpusCollector import CorpusCollector

class MarkovBot:
    def __init__(self, topic): # path to corpus
        self.transition = {}
        self.start_words = []
        self.api = oauth()
        self.init_corpus(topic)
        
    def init_corpus(self, topic):
        collector = CorpusCollector(topic)
        if not os.path.exists(collector.file_name):
            old_dump = collector.get_dump_or_create_new()
            new_batch = collector.get_new_articles()
            old_dump = old_dump.append(new_batch)
            collector.dump(old_dump)

        corpus = pd.read_csv(collector.file_name)['article_name'].values
        
        for line in corpus:
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
        while len(tweet) > 140 or len(tweet.split()) < 7:
            tweet = self.generate()
        return tweet
