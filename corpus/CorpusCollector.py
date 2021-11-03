import sys
import logging
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from utils.config import HOST, FILE_FORMAT, FILE_POSTFIX, DB_LOCATION, COLUMNS, PROXIES

class CorpusCollector:
    """
    Creates a corpus of articles from scratch or appends new articles to an existing one.
    One collector for each topic
    """
    def __init__(self, topic: str):
        self.topic = topic
        self.db_path = os.path.join(
            os.path.abspath('./'),
            DB_LOCATION)

        if not os.path.exists(self.db_path):
            os.mkdir(self.db_path)

        self.file_name = os.path.join(
            self.db_path,
            f'{self.topic}{FILE_POSTFIX}.{FILE_FORMAT}'
            )

        self.session = requests.session()
        self.session.mount(HOST, adapter=requests.adapters.HTTPAdapter(max_retries=5))

        self.max_page = 1
    
    def get_dump_or_create_new(self) -> pd.DataFrame:
        if os.path.exists(self.file_name):
            articles_df = pd.read_csv(self.file_name)
            self.max_page = articles_df['page'].max()
        else:
            articles_df = pd.DataFrame(columns=COLUMNS)
            self.max_page = 1

        return articles_df

    def parse_page(self, page: int) -> pd.DataFrame:
        url = '/'.join([HOST, self.topic, str(page)])

        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
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

    def collect(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=COLUMNS)

        page = self.max_page

        while True:
            try:
                if not page % 100:
                    logging.info(page)
                articles_df = self.parse_page(page)
                df = df.append(articles_df)
                page += 1
            except:
                logging.info(f'Max page is {page - 1}')
                break

        return df

    def dump(self, df: pd.DataFrame):
        df \
            .reset_index(drop=True) \
            .to_csv(self.file_name, index=False)
