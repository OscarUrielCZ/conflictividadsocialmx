import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform(filename):
    logger.info('Initializing transform stage')

    df = _read_data(filename)
    df = _add_news_site(df, filename)
    df = _extract_host(df)

    print(df.news_site)

def _read_data(filename):
    return pd.read_csv(filename)


def _add_news_site(df, filename):
    if 'news_site' in df:
        return df

    news_site_id = filename.split('_')[3]
    if news_site_id == 'eluniversal':
        df['news_site'] = 'https://www.eluniversal.com.mx'
    elif news_site_id == 'elpais':
        df['news_site'] = 'https://elpais.com'
    return df

def _extract_host(df):
    pass
