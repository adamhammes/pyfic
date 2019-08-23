import requests
from lxml import html
from web import web
from sources.tuples import Book, Chapter
from sources.scraper import Scraper

TOC_URL = "https://practicalguidetoevil.wordpress.com/table-of-contents/"


class PracticalGuideToEvil(Scraper):
    @staticmethod
    def matches(url):
        return "practicalguidetoevil" in url

    @staticmethod
    def get_chapter_links(toc_tree, book_num):
        selector = f":contains('Book {book_num}') + ul a"
        return [a.get("href") for a in toc_tree.cssselect(selector)]

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)
        title = tree.cssselect(".entry-title")[0].text

        content_nodes = tree.cssselect(".entry-content p")
        content = "".join(map(Scraper.elem_tostring, content_nodes))
        return Chapter(title=title, text=content)

    def make_book(self, url):
        book_num = url.split("-")[1]
        toc = requests.get(TOC_URL)
        toc_tree = html.fromstring(toc.content, book_num)

        meta = {"author": "ErraticErrata"}
        title = f"A Practical Guide to Evil - Book {book_num}"
        chapter_links = PracticalGuideToEvil.get_chapter_links(toc_tree, book_num)
        chapter_pages = web.download_async(chapter_links)
        chapters = list(map(PracticalGuideToEvil.make_chapter, chapter_pages))

        return Book(title, title, "en-US", meta, chapters)
