from web import web
import requests
from lxml import html
from sources.tuples import *
from sources.scraper import Scraper


class FanficsMe(Scraper):
    @staticmethod
    def matches(url):
        return "fanfics.me" in url

    def make_book(self, page):
        links = [
            "http://fanfics.me/read2.php?id=190897&chapter={}".format(i)
            for i in range(23)
        ]
        pages = web.download_async(links)
        trees = list(map(html.fromstring, pages))

        chapter_texts = list(map(FanficsMe.extract_content, trees))
        chapters = []
        for chapter_num, chapter_text in enumerate(chapter_texts):
            chapter_title = "Chapter {}".format(chapter_num + 1)
            chapters.append(Chapter(chapter_title, chapter_text))

        title = "Harry Potter and the Boy Who Lived "
        book_id = "fanficsme - " + title
        meta = {"author": "The Santi"}
        locale = "en-US"
        return Book(title, book_id, locale, meta, chapters)

    @staticmethod
    def extract_content(tree):
        chapter_node = tree.cssselect(".chapter")[0]
        return Scraper.elem_tostring(chapter_node)
