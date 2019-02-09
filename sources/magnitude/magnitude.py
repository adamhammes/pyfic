from web import web
import requests
from lxml import html
from sources.tuples import *
from sources.scraper import Scraper


class OrdersOfMagnitude(Scraper):
    def __init__(self):
        super().__init__()

        self.TITLE = "Orders of Magnitude"
        self.METADATA = {"author": "NanashiSaito"}

    @staticmethod
    def matches(url):
        return "2pih.com" in url

    @staticmethod
    def generate_links():
        page = requests.get("http://www.2pih.com/table-of-contents/").content
        tree = html.fromstring(page)
        a_links = tree.cssselect("#post-122 > div > ul a")
        return [link.get("href") for link in a_links]

    @staticmethod
    def get_chapter_title(tree):
        return tree.cssselect(".entry-title")[0].text

    @staticmethod
    def get_chapter_text(tree):
        nodes = tree.cssselect(".entry-content > *")
        return "".join(map(Scraper.elem_tostring, nodes))

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)
        title = OrdersOfMagnitude.get_chapter_title(tree)
        content = OrdersOfMagnitude.get_chapter_text(tree)
        return Chapter(title, content)

    def make_book(self, _):
        urls = OrdersOfMagnitude.generate_links()
        print(urls)
        pages = web.download_async(urls)

        chapters = list(map(OrdersOfMagnitude.make_chapter, pages))

        return Book(self.TITLE, self.get_id(), "en-US", self.METADATA, chapters)
