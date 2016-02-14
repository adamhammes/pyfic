import requests
from lxml import etree, html
from ..tuples import Chapter

HOME_PAGE = 'https://unillustrated.wordpress.com/'


def generate_links():
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect('#linkcat-283635721 a'):
        yield node.get('href')


def spanless(node):
    return all(child.tag != 'span' for child in node)


def extract_content(tree):
    nodes = filter(spanless, tree.cssselect('.entry-content p'))
    raw_bytes = b''.join(map(etree.tostring, nodes))
    return str(raw_bytes, encoding='UTF-8')


def extract_title(tree):
    return tree.cssselect('.entry-title')[0].text


def make_chapter(html_string):
    tree = html.fromstring(html_string)
    title = extract_title(tree)
    text = extract_content(tree)
    return Chapter(title, text)
