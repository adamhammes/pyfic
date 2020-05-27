import requests
from lxml import html
from web import web
from sources.tuples import Book, Chapter
from sources.scraper import Scraper

BOOK_URL = "https://archiveofourown.org/works/11478249/chapters/"
ending_chapters = [0, 14, 33, 52, 75, 105, 138, 195]


class WorthTheCandle(Scraper):
    @staticmethod
    def matches(url):
        if not "worththecandle" in url:
            return False

        num_books = len(ending_chapters) - 1
        index = int(url.split("-")[1])

        if not 1 <= index <= num_books:
            print(f"No ending chapter found for book {index} of Worth the Candle :-(")
            return False

        return True

    @staticmethod
    def get_chapter_links(book_index):
        start, stop = ending_chapters[book_index - 1], ending_chapters[book_index]
        chapter_indices = list(range(start, stop))

        tree = html.fromstring(requests.get(BOOK_URL).content)

        toc_elems = tree.cssselect("#chapter_index option")
        links = [BOOK_URL + option.get("value") for option in toc_elems]

        return [links[index] for index in chapter_indices]

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)
        title_node = tree.cssselect("#selected_id [selected='selected']")[0]
        _, title = title_node.text.split(" ", 1)

        content_container = tree.cssselect("[role='article']")[0]
        content_nodes = [node for node in content_container if node.tag != "h3"]
        content = "".join(map(Scraper.elem_tostring, content_nodes))
        return Chapter(title=title, text=content)

    def make_book(self, url):
        book_num = int(url.split("-")[1])
        chapter_links = WorthTheCandle.get_chapter_links(book_num)

        chapter_pages = web.download_async(chapter_links)
        chapters = list(map(WorthTheCandle.make_chapter, chapter_pages))

        meta = {"author": "cthulhuraejepsen"}
        title = f"Worth the Candle - Book {book_num}"
        return Book(title, title, "en-US", meta, chapters)
