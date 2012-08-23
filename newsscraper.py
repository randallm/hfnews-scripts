from urlparse import urlparse
from time import sleep
from random import uniform
from bs4 import BeautifulSoup
from readability.readability import Document
import requests
import feedparser


class NewsScraper(object):
    """Takes XML feed information and scrapes content from articles in feed"""
    def __init__(self, xml_feed_url):
        self.xml_feed_url = xml_feed_url

        self.raw_xml = feedparser.parse(self.xml_feed_url)
        self.raw_links = None
        self.permalinks = None
        self.title_list = None
        self.raw_html = []
        self.article_html = []

    def fetch_raw_links(self):
        """Fetches article links from XML RSS feed"""
        self.raw_links = [entry.link for entry in self.raw_xml.entries]
        return self.raw_links

    @staticmethod
    def remove_url_params(dirty_url):
        """Removes extra (referrer) parameters at end of URL"""
        return (urlparse(dirty_url).scheme +
                '://' +
                urlparse(dirty_url).netloc +
                urlparse(dirty_url).path)

    def fetch_permalinks(self):
        """Takes list of article URLs, converts to list of permalinks"""
        self.permalinks = [requests.get(link).url for link in self.raw_links]
        self.permalinks = [self.remove_url_params(link) for link
                           in self.permalinks]
        return self.permalinks

    def fetch_titles(self):
        """Takes XML RSS feed, outputs names of articles"""
        self.title_list = [entry.title for entry in self.raw_xml.entries]
        return self.title_list

    def fetch_raw_html(self):
        """
        Goes through permalinks list, outputs raw HTML list of an article.
        Each list entry has a string type.
        """
        # self.raw_html = [requests.get(link).content for link
        #                  in self.permalinks]
        for link in self.permalinks:
            self.raw_html.append(requests.get(link).content)
            sleep(uniform(.5, 3))
        return self.raw_html

    def fetch_article_contents(self):
        """
        Uses Readability.js + BS4 methods to parse raw html list and
        outputs list of text in an article
        """
        for article in self.raw_html:
            article = Document(article).summary()
            article = BeautifulSoup(article)
            [tag.extract() for tag in article.find_all('img')]
            [tag.extract() for tag in article.find_all('embed')]
            article = article.get_text()
            article = unicode(article)
            article = article.replace('\t', '')
            article = article.replace('\n', ' ')
            self.article_html.append(article)
        return self.article_html


def fetch_articles(xml_feed_url):
    """Puts together all other functions and prints lists to screen"""
    scraper = NewsScraper(xml_feed_url)

    scraper.fetch_raw_links()
    scraper.fetch_permalinks()
    scraper.fetch_titles()
    scraper.fetch_raw_html()
    scraper.fetch_article_contents()

    print '\nArticle Permalinks:\n'
    print scraper.permalinks

    print '\nArticle Titles:\n'
    print  scraper.title_list

    print '\nArticles:\n'
    print scraper.article_html
