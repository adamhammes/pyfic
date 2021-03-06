import requests
import cssselect
from lxml import html
from sources.tuples import *
from sources.scraper import Scraper
from web import web


BASE_URL = "https://www.parahumans.net/"
METADATA = {"author": "Wildbow"}


class Ward(Scraper):
    @staticmethod
    def matches(url):
        return "parahumans.net" in url and not "wordpress" in url

    @staticmethod
    def get_chapter_links():
        toc = BASE_URL + "table-of-contents"
        tree = html.fromstring(requests.get(toc).content)

        anchors = tree.cssselect(".entry-content a")
        return [anchor.get("href") for anchor in anchors]

    @staticmethod
    def contains_link(node):
        """
        Returns `True` if `node` contains any links. Recursively checks children, grand-children, and so on.
        """
        return any(child.tag == "a" for child in node.iter())

    @staticmethod
    def is_nav_link(node):
        """
        Returns `True` if the node contains the navigation links to the previous and next chapters.
        """
        nav_names = ["Next Chapter", "Previous Chapter", "Next", "Previous"]
        return any(
            name in node.text_content() for name in nav_names
        ) and Ward.contains_link(node)

    @staticmethod
    def make_pretty(content):
        no_links = (
            paragraph for paragraph in content if not Ward.is_nav_link(paragraph)
        )
        stringified = map(Scraper.elem_tostring, no_links)
        return "".join(stringified)

    def make_chapter(self, page):
        tree = html.fromstring(page)
        paragraphs = tree.cssselect(".entry-content p")
        title = tree.cssselect(".entry-title")[0].text_content()
        prettified = self.make_pretty(paragraphs)
        return Chapter(title, prettified)

    def make_book(self, _):
        chapter_links = Ward.get_chapter_links()
        chapter_pages = web.download_async(chapter_links)
        chapters = [self.make_chapter(page) for page in chapter_pages]
        return Book("Ward", self.get_id(), self.LANGUAGE, METADATA, chapters)
