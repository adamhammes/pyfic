import re
import time
import requests
from sources.scraper import Scraper
from lxml import html
from sources.tuples import Book, Chapter
from web import web


class FanfictionDotNet(Scraper):
    @staticmethod
    def matches(url):
        return 'fanfiction.net' in url

    @staticmethod
    def _canonical_url(tree):
        full_link = tree.cssselect('link[rel=canonical]')[0].get('href')
        regex = '\/\/(www.fanfiction.net\/s/\d+\/)'
        return 'http://' + re.match(regex, full_link).group(1)

    @staticmethod
    def generate_links(page):
        tree = html.fromstring(page)
        url = FanfictionDotNet._canonical_url(tree)
        option_links = tree.cssselect('#chap_select option')
        chapter_values = (option.get('value') for option in option_links)
        return [url + value for value in chapter_values]

    @staticmethod
    def extract_content(tree):
        nodes = tree.cssselect('.storytext p')
        return ''.join(map(Scraper.elem_tostring, nodes))

    @staticmethod
    def get_title(tree):
        return tree.cssselect('#profile_top > b')[0].text

    @staticmethod
    def get_chapter_title(tree):
        regex = '\d+. (.*)'
        title_elem = tree.cssselect('#chap_select option[selected]')[0]
        return re.search(regex, title_elem.text).group(1)

    @staticmethod
    def get_id(tree):
        url = FanfictionDotNet._canonical_url(tree)
        regex = '.*/s/(\d+)'
        story_id = re.search(regex, url).group(0)
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        return 'fanfiction.net:{} on {}'.format(story_id, time_str)

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)
        title = FanfictionDotNet.get_chapter_title(tree)
        content = FanfictionDotNet.extract_content(tree)
        return Chapter(title, content)

    @staticmethod
    def get_author(tree):
        return tree.cssselect('#profile_top > a:nth-child(5)')[0].text

    def make_book(self, url):
        links = FanfictionDotNet.generate_links(requests.get(url).content)
        pages = web.download_async(links)
        first_tree = html.fromstring(pages[0])
        title = FanfictionDotNet.get_title(first_tree)
        book_id = FanfictionDotNet.get_id(first_tree)
        meta = {'author': FanfictionDotNet.get_author(first_tree)}

        chapters = list(map(FanfictionDotNet.make_chapter, pages))
        return Book(title, book_id, 'en-US', meta, chapters)
