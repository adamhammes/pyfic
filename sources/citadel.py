"""
A module for screen scraping the book Citadel, found on https://unillustrated.wordpress.com/
"""
import time
import requests
from lxml import etree, html
from .tuples import *
from web import web

HOME_PAGE = 'https://unillustrated.wordpress.com/'
TITLE = 'Citadel: Training in Necessity'
LINK_SELECTOR = '#linkcat-283635721 a'
CONTENT_SELECTOR = '.entry-content p'
TITLE_SELECTOR = '.entry-title'

METADATA = {
    'author': 'Unillustrated'
}


def generate_links():
    """
    Find the links for each chapter
    :return: List of strings corresponding to the link for each chapter
    """
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect(LINK_SELECTOR):
        yield node.get('href')


def _spanless(node):
    """
    Check if a direct child is a span
    :param node: Node to check
    :return: True if no children are a span element
    """
    return all(child.tag != 'span' for child in node)


def extract_content(tree):
    """
    Extract the content for a chapter
    :param tree: The lxml tree object corresponding to the chapter
    :return: A string containing the html of the content
    """
    nodes = filter(_spanless, tree.cssselect(CONTENT_SELECTOR))
    raw_bytes = b''.join(map(etree.tostring, nodes))
    return str(raw_bytes, encoding='UTF-8')


def extract_title(tree):
    """
    Find the title for a chapter
    :param tree: The lxml tree object corresponding to the chapter
    :return: The title of the chapter as a string
    """
    return tree.cssselect(TITLE_SELECTOR)[0].text


def make_chapter(html_string):
    """
    Create a chapter from its corresponding web page
    :param html_string: the html for the chapter
    :return: a Chapter corresponding to the given page
    """
    tree = html.fromstring(html_string)
    title = extract_title(tree)
    text = extract_content(tree)
    return Chapter(title, text)


def get_id():
    """
    Generate a unique id for the book, based on the title and time of access
    :return: The book's unique id
    """
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    return '{0} {1}'.format(TITLE, time_str)


def make_book():
    """
    Create an up-to-date copy of the book Citadel
    :return: a Book corresponding to what is published online
    """
    pages = web.download_async(generate_links())
    chapters = [make_chapter(page) for page in pages]
    return Book(TITLE, get_id(), 'en-US', METADATA, chapters)
