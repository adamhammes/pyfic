import time
import requests
from lxml import etree, html
from ..tuples import Chapter
from web import web

HOME_PAGE = 'https://unillustrated.wordpress.com/'
TITLE = 'Citadel: Training in Necessity'
LINK_SELECTOR = '#linkcat-283635721 a'
CONTENT_SELECTOR = '.entry-content p'
TITLE_SELECTOR = '.entry-title'


def generate_links():
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect(LINK_SELECTOR):
        yield node.get('href')


def spanless(node):
    return all(child.tag != 'span' for child in node)


def extract_content(tree):
    nodes = filter(spanless, tree.cssselect(CONTENT_SELECTOR))
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


def get_metadata():
    return {}


def make_book():
    pages = web.download_async(generate_links())
    chapters = map(make_chapter, pages)
    return Chapter(TITLE, get_id(), get_metadata(), chapters)
