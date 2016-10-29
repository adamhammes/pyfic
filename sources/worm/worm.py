import time
import xml.etree.cElementTree as etree
from lxml import html
from sources.tuples import *
from web import web

from .links import links, titles


class Worm:
    def __init__(self):
        self.TITLE = 'Worm'

        self.METADATA = {
            'author': 'Wildbow',
        }

    @staticmethod
    def matches(url):
        return url.contains('parahumans.wordpress.com')

    @staticmethod
    def elem_tostring(elem):
        return etree.tostring(elem, encoding='unicode')

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
        nav_names = ['Next Chapter', 'Previous Chapter', 'Next']
        return any(name in node.text_content() for name in nav_names) and Worm.contains_link(node)

    @staticmethod
    def make_pretty(content):
        no_links = (paragraph for paragraph in content if not Worm.is_nav_link(paragraph))
        stringified = map(Worm.elem_tostring, no_links)
        return ''.join(stringified)

    def make_chapter(self, title, page):
        tree = html.fromstring(page)
        paragraphs = tree.cssselect('article p')
        prettified = self.make_pretty(paragraphs)
        return Chapter(title, prettified)

    def get_id(self):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        return '{0} {1}'.format(self.TITLE, time_str)

    def make_book(self):
        pages = web.download_async(links)
        chapters = [self.make_chapter(title, page) for title, page in zip(titles, pages)]

        return Book(self.TITLE, self.get_id(), 'en-US', self.METADATA, chapters)
