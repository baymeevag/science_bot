from random import randint, choice
import tweepy, time, webbrowser, re

class MarkovBot:
    def __init__(self, path_to_secret, path_to_corpus, tweets_a_day): # path to corpus
        self.sleep_timer = int(60 * 60 * tweets_a_day)
        self.transition = {}
        self.start_words = []
        self.api = tweepy.API()
        self.oauth(path_to_secret)
        self.init_corpus(path_to_corpus)
        
    def oauth(self, path_to_secret):
        with open(path_to_secret) as f:
            consumer_key_secret = f.readlines()
        consumer_key_secret = [x.strip() for x in consumer_key_secret] 
        consumer_key = consumer_key_secret[0]
        consumer_secret = consumer_key_secret[1]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth_url = auth.get_authorization_url()
        webbrowser.open(auth_url)
        verifier = raw_input('PIN: ').strip()
        auth.get_access_token(verifier)
        with open('./access_key_secret.txt', 'w') as f:
            f.write(auth.access_token + '\n' + auth.access_token_secret)
        self.api = tweepy.API(auth)
        
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


if __name__ == '__main__':
    bot = MarkovBot('./consumer_key_secret.txt', './cyberleninka_all.txt', 3)
    bot.run()

