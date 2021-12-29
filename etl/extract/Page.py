import requests
import bs4

class Page:
    def __init__(self, url):
        self._url = url
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        self._html = None
        self._visit()
    
    def __str__(self):
        legend = 'processed' if self._html is not None else 'not processed yet'
        return f'{self._url} {legend}'

    def _visit(self):
        response = requests.get(self._url, headers=self.__headers)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _select(self, query):
        for elem in self._html.select(query):
            yield elem
        

class Homepage(Page):
    def __init__(self, url, queries):
        super().__init__(url)
        self.__article_links_query = queries.get('homepage_article_links')

    @property
    def article_links(self):
        """Get all articles from a news home page. You need to call the visit() method before."""
        if self._html is None:
            return None
        link_list = []
        for link in self._select(self.__article_links_query):
            if link and link.has_attr('href'):
                link_list.append(link['href'])
        return set(link_list)

class ArticlePage(Page):
    def __init__(self, url, queries, news_site):
        super().__init__(url)
        self.__news_site = news_site
        self.__title_query = queries.get('article_title')
        self.__date_query = queries.get('article_date')
        self.__time_query = queries.get('article_time')
        self.__location_query = queries.get('article_location')
        self.__body_query = queries.get('article_body')
        self.__image_query = queries.get('article_image')

    @property
    def title(self):
        # result = self._select(self.__title_query)
        # return result[0].text if len(result) else ''
        if not self.__title_query:
            return ''
        result = next(self._select(self.__title_query), None)
        return result.text if result else ''

    @property
    def date(self):
        if not self.__date_query:
            return ''
        result = next(self._select(self.__date_query), None)
        return result.text if result else ''

    @property
    def time(self):
        if not self.__time_query:
            return ''
        result = next(self._select(self.__time_query), None)
        return result.text if result else ''

    @property
    def location(self):
        if not self.__location_query:
            return ''
        result = next(self._select(self.__location_query), None)
        return result.text if result else ''

    @property
    def image(self):
        if not self.__image_query:
            return ''
        result = next(self._select(self.__image_query), None)
        return result['src'] if result else ''

    @property
    def body(self):
        # result = self._select(self.__body_query)
        # return result[0].text if len(result) else ''
        if not self.__body_query:
            return ''
        result = next(self._select(self.__body_query), None)
        return result.text if result else ''
    
    @property
    def url(self):
        return self._url

    @property
    def news_site(self):
        return self.__news_site