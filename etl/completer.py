import argparse
import logging
import requests
import bs4

from extract.load import load_file
from utils.utils import article_page_headers, get_exception_message

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__data_filename = 'extract/sites.yaml'

def main(filename):
    logger.info('Reprocessing file ' + filename)

    df = pd.read_csv(filename)
    news_site = _get_news_site(filename)
    
    # insert news_site column
    if 'news_site' not in df:
        df['news_site'] = news_site

    data = load_file(__data_filename).get('news_sites').get(news_site)

    if not data:
        logger.error('No info into the filename')
        return

    queries = data.get('queries')
    df = df.apply(lambda article: _get_article_info(article, queries), axis=1)
    df.to_csv(_get_recovered_filename(filename), index=False)
    logger.info('CSV file with recovered values created')

def _get_article_info(article, queries):
    '''
        Parameters
            article: article info as a pandas serie
            data: the data related to the news site
    '''

    get_element = lambda html, query: html.select(query)

    try:
        response = requests.get(article.url, headers=article_page_headers)
        response.raise_for_status()
        html = bs4.BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.warning(f'Cannot get article info from {article.url}')
        return article

    query_names = {
        'title': 'article_title',
        'body': 'article_body',
        'date': 'article_date',
        'time': 'article_time',
        'location': 'article_location',
        'image': 'article_image'
    }

    empty_columns = article[article.isnull()].index
    recovered_cols = 0

    for col in empty_columns:
        query_name = query_names.get(col)
        if not query_name: continue
        query = queries.get(query_name)
        if not query: continue
        element = get_element(html, query)
        if len(element) == 0: continue

        if col == 'image': element = element[0]['src']
        else: element = element[0].text

        article[col] = element
        recovered_cols += 1

    logger.info(f'{recovered_cols}/{len(empty_columns)} recovered columns from {article.url}')

    return article

def _get_recovered_filename(filename):
    parts = filename.split('.')
    ext = parts[-1]
    return '.'.join(parts[0:-1])+'_recovered.'+ext

def _get_news_site(filename):
    return filename.split('_')[3]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename to re-extract info", type=str)
    arg = parser.parse_args()
    main(arg.filename)