import requests
import os
import sys
sys.path.append('.')
sys.path.append('..')
import re
from bs4 import BeautifulSoup
import pandas as pd
import pickle
from utils.logger_config import logger_config
from utils.config import HOST, FILE_FORMAT, FILE_POSTFIX, DB_LOCATION, COLUMNS

class CorpusCollector:
    """
    Creates a corpus of articles from scratch or appends new articles to an existing one.
    One collector for each topic
    """
    def __init__(self, topic):
        self.logger = logger_config()
        self.schema = COLUMNS
        self.topic = topic
        self.file_name = os.path.join(
            DB_LOCATION,
            f'{self.topic}{FILE_POSTFIX}.{FILE_FORMAT}'
            )
    
    def get_dump_or_create_new(self):
        if os.path.exists(self.file_name):
            articles_df = pd.read_csv(self.file_name)
            self.max_page = articles_df['page'].max()
        else:
            articles_df = pd.DataFrame(columns=COLUMNS)
            self.max_page = 1

        return articles_df

    def parse_page(self, page):
        url = '/'.join([HOST, self.topic, str(page)])
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        article_list = soup.findAll('div', {'class': 'title'})
        articles = [article.text for article in article_list]

        if len(articles) == 0:
            raise Exception(f'Reached the end of {self.topic}')

        articles_df = pd.DataFrame(
            {
                'topic': [self.topic] * len(articles), 
                'page': [page] * len(articles),
                'article_name': articles
            }, 
            columns=COLUMNS
        )

        return articles_df

    def get_new_articles(self):
        df = pd.DataFrame(columns=COLUMNS)

        page = self.max_page

        while True:
            try:
                if not page % 100:
                    self.logger.info(page)
                articles_df = self.parse_page(page)
                df = df.append(articles_df)
                page += 1
            except (KeyboardInterrupt, Exception) as e:
                print(e)
                self.logger.info(f'Max page is {page - 1}')
                break

        return df

    def dump(self, df):
        df \
            .reset_index(drop=True) \
            .to_csv(self.file_name, index=False)
