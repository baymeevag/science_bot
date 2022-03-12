from random import randint, choice
import tweepy
import time
import pandas as pd
import os
from corpus.CorpusCollector import CorpusCollector
from utils.config import START_TOKEN, END_TOKEN


class Markov:
    def __init__(self, topic):  # path to corpus
        self.transition = {}
        self._init_corpus(topic)

    def _init_corpus(self, topic):
        collector = CorpusCollector(topic)
        corpus = pd.read_csv(collector.file_name)["article_name"].values

        for line in corpus:
            words = [START_TOKEN] + line.split() + [END_TOKEN]
            for word1, word2 in zip(words[:-1], words[1:]):
                if word1 in self.transition:
                    self.transition[word1].append(word2)
                else:
                    self.transition[word1] = [word2]

    def generate(self, seed=None):
        result = seed.split() if seed else [START_TOKEN]
        current_word = result[-1]
        while (
            current_word in self.transition.keys()
            and self.transition[current_word]
            and current_word != END_TOKEN
        ):
            current_word = choice(self.transition[current_word])
            result.append(current_word)
        return " ".join(result[0 if seed else 1 : -1])

    def get_tweet(self, seed=None):
        tweet = self.generate(seed)
        while len(tweet) > 140 or len(tweet.split()) < 5:
            tweet = self.generate(seed)
        return tweet
