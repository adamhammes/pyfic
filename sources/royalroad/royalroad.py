import time
import requests
from sources.scraper import Scraper
from lxml import html
from sources.tuples import Book, Chapter
from web import web

BASE_URL = "http://www.royalroad.com"


class RoyalRoadScraper(Scraper):
    @staticmethod
    def matches(url):
        return "royalroad.com" in url

    @staticmethod
    def generate_links(tree):
        anchors = tree.cssselect("#chapters td:first-child a")
        return [BASE_URL + anchor.get("href") for anchor in anchors]

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)
        title = tree.cssselect("h1")[0].text
        p_tags = tree.cssselect(".chapter-content > p")

        cleaned_ps = []
        for p in p_tags:
            p.attrib.pop("style", None)
            spans = p.cssselect("span")
            if spans:
                spans[0].attrib.pop("style", None)

            p_text = "".join(p.itertext()).strip()
            if p_text:
                cleaned_ps.append(p)

        content = "".join(map(Scraper.elem_tostring, cleaned_ps))

        return Chapter(title, content)

    def make_book(self, url):
        page = requests.get(url).content
        tree = html.fromstring(page)
        links = RoyalRoadScraper.generate_links(tree)
        pages = web.download_async(links)
        title = tree.cssselect('[property="name"]')[0].text

        author = tree.cssselect('[property="name"] a')[0].text
        meta = {"author": author}
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        book_id = url.split("/")[-2] + time_str
        chapters = list(map(RoyalRoadScraper.make_chapter, pages))

        return Book(title, book_id, "en-US", meta, chapters)

