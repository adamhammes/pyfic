"""
A module for screen scraping the book Citadel, found on https://unillustrated.wordpress.com/
"""
import requests
from lxml import html
from sources.tuples import Book, Chapter
from sources.scraper import Scraper
from web import web

HOME_PAGE = 'https://unillustrated.wordpress.com/'
TITLE = 'Citadel: Training in Necessity'
TITLE_SELECTOR = '.entry-title'

METADATA = {
    'author': 'Unillustrated'
}


class Citadel(Scraper):
    @staticmethod
    def matches(url):
        return 'unillustrated.wordpress.com' in url

    @staticmethod
    def generate_links():
        """
        Find the links for each chapter
        :return: List of strings corresponding to the link for each chapter
        """
        link_selector = '#linkcat-283635721 a'

        page = requests.get(HOME_PAGE)
        tree = html.fromstring(page.content)
        for node in tree.cssselect(link_selector):
            yield node.get('href')

    @staticmethod
    def _spanless(node):
        """
        Check if a direct child is a span
        :param node: Node to check
        :return: True if no children are a span element
        """
        return all(child.tag != 'span' for child in node)

    @staticmethod
    def extract_content(tree):
        """
        Extract the content for a chapter
        :param tree: The lxml tree object corresponding to the chapter
        :return: A string containing the html of the content
        """
        content_selector = '.entry-content p'
        nodes = filter(Citadel._spanless, tree.cssselect(content_selector))
        return ''.join(map(Scraper.elem_tostring, nodes))

    @staticmethod
    def extract_title(tree):
        """
        Find the title for a chapter
        :param tree: The lxml tree object corresponding to the chapter
        :return: The title of the chapter as a string
        """
        return tree.cssselect(TITLE_SELECTOR)[0].text

    @staticmethod
    def make_chapter(html_string):
        """
        Create a chapter from its corresponding web page
        :param html_string: the html for the chapter
        :return: a Chapter corresponding to the given page
        """
        tree = html.fromstring(html_string)
        title = Citadel.extract_title(tree)
        text = Citadel.extract_content(tree)
        return Chapter(title, text)

    @staticmethod
    def make_book(self):
        """
        Create an up-to-date copy of the book Citadel
        :return: a Book corresponding to what is published online
        """
        pages = web.download_async(Citadel.generate_links())
        chapters = [Citadel.make_chapter(page) for page in pages]
        return Book(TITLE, self.get_id(), 'en-US', METADATA, chapters)
