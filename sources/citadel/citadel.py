import requests
from lxml import etree, html


HOME_PAGE = 'https://unillustrated.wordpress.com/'


def generate_links():
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect("#linkcat-283635721 a"):
        yield node.get('href')


def extract_content(html_string):
    tree = html.fromstring(html_string)
    nodes = tree.cssselect(".entry-content p")
    return b''.join(map(etree.tostring, nodes))
