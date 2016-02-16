import time
import requests
from lxml import etree, html
from ..tuples import Chapter, Book
from web import web

HOME_PAGE = 'https://unillustrated.wordpress.com/'
TITLE = 'Citadel: Training in Necessity'
LINK_SELECTOR = '#linkcat-283635721 a'
CONTENT_SELECTOR = '.entry-content p'
TITLE_SELECTOR = '.entry-title'

METADATA = {}


def generate_links():
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect(LINK_SELECTOR):
        yield node.get('href')


def _spanless(node):
    return all(child.tag != 'span' for child in node)


def extract_content(tree):
    nodes = filter(_spanless, tree.cssselect(CONTENT_SELECTOR))
    raw_bytes = b''.join(map(etree.tostring, nodes))
    return str(raw_bytes, encoding='UTF-8')


def extract_title(tree):
    return tree.cssselect(TITLE_SELECTOR)[0].text


def make_chapter(html_string):
    tree = html.fromstring(html_string)
    title = extract_title(tree)
    text = extract_content(tree)
    return Chapter(title, text)


def get_id():
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    return '{0} {1}'.format(TITLE, time_str)


def make_book():
    pages = web.download_async(generate_links())
    chapters = [make_chapter(page) for page in pages]
    return Book(TITLE, get_id(), 'en-US', METADATA, chapters)
