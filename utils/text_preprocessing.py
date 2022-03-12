from typing import List
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
import nltk

nltk.download("stopwords")

stem = SnowballStemmer("russian")

russian_stopwords = stopwords.words("russian")
english_stopwords = stopwords.words("english")


def preprocessing(text: str) -> List[str]:
    tokens = text.lower().split()
    filtered_tokens = list(
        filter(
            lambda x: x
            not in russian_stopwords + english_stopwords + list(punctuation),
            tokens,
        )
    )
    return list(map(lambda x: stem.stem(x), filtered_tokens))
