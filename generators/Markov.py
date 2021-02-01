from random import randint, choice
import tweepy
import time
import pandas as pd
import re
import os
import sys
from corpus.CorpusCollector import CorpusCollector

class Markov:
    def __init__(self, topic): # path to corpus
        self.transition = {}
        self.start_words = []
        self._init_corpus(topic)
        
    def _init_corpus(self, topic):
        collector = CorpusCollector(topic)
        corpus = pd.read_csv(collector.file_name)['article_name'].values
        
        for line in corpus:
            words = line.split()
            self.start_words.append(words[0])
            for word1, word2 in zip(words[:-1], words[1:]):
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
