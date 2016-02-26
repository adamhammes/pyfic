import re
import time
import requests
from lxml import etree, html
from tuples import Book, Chapter
from web import web


def _canonical_url(tree):
    full_link = tree.cssselect('link[rel=canonical]')[0].get('href')
    regex = '\/\/(www.fanfiction.net\/s/\d+\/)'
    return 'http://' + re.match(regex, full_link).group(1)


def generate_links(page):
    tree = html.fromstring(page)
    url = _canonical_url(tree)
    option_links = tree.cssselect('#chap_select option')
    chapter_values = (option.get('value') for option in option_links)
    return [url + value for value in chapter_values]


def extract_content(page):
    tree = html.fromstring(page)
    nodes = tree.cssselect('#storytext p')
    raw_bytes = b''.join(map(etree.tostring, nodes))
    return str(raw_bytes, encoding='UTF-8')


def get_title(tree):
    print(_canonical_url(tree))
    return tree.cssselect('#profile_top > b')[0].text


def get_id(tree):
    url = _canonical_url(tree)
    regex = '.*/s/(\d+)'
    story_id = re.search(regex, url).group(0)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    return 'fanfiction.net:{0} on {1}'.format(story_id, time_str)


def get_author(tree):
    return tree.cssselect('#profile_top > a:nth-child(4)')[0].text


def make_book(url):
    links = generate_links(requests.get(url).content)
    pages = web.download_async(links)
    first_tree = html.fromstring(pages[0])
    title = get_title(first_tree)
    book_id = get_id(first_tree)
    meta = {'author': get_author(first_tree)}

    return Book(title, book_id, 'en-US', meta, pages)


if __name__ == '__main__':
    make_book('http://www.fanfiction.net/s/2636963/2/')
