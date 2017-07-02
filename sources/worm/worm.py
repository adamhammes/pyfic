from lxml import html
from sources.tuples import *
from sources.scraper import Scraper
from web import web

from .links import links, titles


class Worm(Scraper):
    def __init__(self):
        super().__init__()

        self.TITLE = 'Worm'

        self.METADATA = {
            'author': 'Wildbow',
        }

    @staticmethod
    def matches(url):
        return 'parahumans.wordpress.com' in url

    @staticmethod
    def contains_link(node):
        """
        Returns `True` if `node` contains any links. Recursively checks children, grand-children, and so on.
        """
        return any(child.tag == 'a' for child in node.iter())

    @staticmethod
    def is_nav_link(node):
        """
        Returns `True` if the node contains the navigation links to the previous and next chapters.
        """
        nav_names = ['Next Chapter', 'Previous Chapter', 'Next', 'Previous']
        return any(name in node.text_content() for name in nav_names) and Worm.contains_link(node)

    @staticmethod
    def make_pretty(content):
        no_links = (paragraph for paragraph in content if not Worm.is_nav_link(paragraph))
        stringified = map(Scraper.elem_tostring, no_links)
        return ''.join(stringified)

    def make_chapter(self, title, page):
        tree = html.fromstring(page)
        paragraphs = tree.cssselect('article p')
        prettified = self.make_pretty(paragraphs)
        return Chapter(title, prettified)

    def make_book(self, _):
        pages = web.download_async(links)
        chapters = [self.make_chapter(title, page) for title, page in zip(titles, pages)]

        cover_location = Scraper.get_relative_path('covers/worm-cover.jpg')
        with open(cover_location, 'rb') as f:
            photo = f.read()

        return Book(self.TITLE, self.get_id(), self.LANGUAGE, self.METADATA, chapters, photo)
