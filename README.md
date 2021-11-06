# Science bot
Twitter bot that generates math articles' names (in Russian) (https://twitter.com/neural_maths)

There are three components to this bot:

### Gathering source text

Sample article names are scrapped from cyberleninka.ru, this part is implemented in HTML_parsing.ipynb. 
Words that contain inappropriate symbols (i.e. Latex source code) and English words are excluded to avoid generating even weirder 
gibberish than it already does.

### Generating text

The bot uses Markov text generator to generate tweets. Starting from a random word, every subsequent word is picked based on how
often it appears in the source text next to the previous one. 


### Posting to twitter

This part is handled with tweepy.

---
To be done: interface for simply generating the text given an arbitrary corpus, instructions.
