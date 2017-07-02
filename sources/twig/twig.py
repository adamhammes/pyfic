import requests
from lxml import html

from sources.scraper import Scraper
from sources.tuples import *
from web import web
from ..worm import Worm

BASE_URL = 'https://twigserial.wordpress.com'


class Twig(Scraper):
    def __init__(self):
        super().__init__()

        self.TITLE = 'Twig'

        self.METADATA = {
            'author': 'Wildbow'
        }

    @staticmethod
    def matches(url):
        return 'twigserial.wordpress.com' in url

    def make_book(self, _):
        chapters = Twig.make_chapters()

        cover_location = Scraper.get_relative_path('covers/twig-cover.jpg')
        with open(cover_location, 'rb') as f:
            photo = f.read()

        return Book(self.TITLE, self.get_id(), self.LANGUAGE, self.METADATA, chapters, photo)

    @staticmethod
    def generate_links():
        page = requests.get(BASE_URL).content
        tree = html.fromstring(page)

        url_base = BASE_URL + '?cat='
        chapter_nodes = tree.cssselect('#cat .level-2')

        return [url_base + node.get('value') for node in chapter_nodes]

    @staticmethod
    def make_chapters():
        links = Twig.generate_links()
        pages = web.download_async(links)

        return list(map(Twig.make_chapter, pages))

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)

        p_nodes = tree.cssselect('.entry-content p')
        content = Worm.make_pretty(p_nodes)

        title = tree.cssselect('.entry-title a')[0].text
        return Chapter(title=title, text=content)
