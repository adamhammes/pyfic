import requests
from lxml import html

HOME_PAGE = 'https://unillustrated.wordpress.com/'


def generate_links():
    page = requests.get(HOME_PAGE)
    tree = html.fromstring(page.content)
    for node in tree.cssselect("#linkcat-283635721 a"):
        yield node.get('href')
