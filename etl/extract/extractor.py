import logging
import re
import datetime
import csv
import os

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from extract.load import load_file
from extract.Page import Homepage, ArticlePage
from utils.utils import get_exception_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r"^https?://.+/.+$")
is_root_path = re.compile(r"^/.+$")
__filename = 'extract/sites.yaml'

def extract(site=None):
    data = load_file(__filename).get('news_sites')

    if not data:
        logger.warning('No info into the filename')
        return

    logger.info("Initializing extract stage")

    dirname = _create_dir()

    if site:
        info = data.get(site)
        url = info.get('url')
        queries = info.get('queries')
        _fetch_news_site(site, url, queries, dirname=dirname)
    else:
        for news_site, info in data.items():
            url = info.get('url')
            queries = info.get('queries')
            _fetch_news_site(news_site, url, queries, dirname=dirname)

def _fetch_news_site(news_site, url, queries, dirname=None):
    logger.info(f'Fetching {news_site}')

    try:
        page = Homepage(url, queries)
    except Exception as e:
        logger.warning(get_exception_message(e))
        return

    article_links = page.article_links
    if not article_links:
        logger.warning(f'No articles found from {news_site}')
        return
    logger.info(f'{len(article_links)} article links extracted from {news_site}')

    articles = []
    for al in article_links:
        article = _fetch_article(news_site, url, al, queries)
        if article:
            articles.append(article)
    logger.info(f'{len(articles)} articles fetched')
    _save_articles(dirname, news_site, articles)

def _fetch_article(news_site, host, article_link, queries):
    full_link = _build_link(host, article_link)
    try:
        article = ArticlePage(full_link, queries, news_site)
    except (HTTPError, MaxRetryError) as e:
        logger.warning(f'Cannot get article from {full_link}')
        return None

    if article and not article.body:
        logger.warning(f'Article with no body {full_link}')
        return None
    logger.info(f'Fetched article {full_link}')
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'

def _create_dir():
    today_date = datetime.date.today().strftime('%Y_%m_%d')
    dirname = os.path.join('data', f'{today_date}_news')
    i = 2

    while os.path.isdir(dirname):
        dirname = os.path.join('data', f'{today_date}_news_{i}')
        i += 1

    os.mkdir(dirname)

    return dirname

def _save_articles(dirname, news_site, articles_list):
    logger.info("Writing articles into csv file")
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = os.path.join(dirname, f'{now}_{news_site}_articles.csv')
    # get attributes of an article (title, body, url)
    csv_headers = list(filter(lambda property: not property.startswith("_"), dir(articles_list[0])))

    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles_list:
            row = [str(getattr(article, property)) for property in csv_headers]
            writer.writerow(row)