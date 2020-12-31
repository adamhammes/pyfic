import requests
from lxml import html
from web import web
from sources.tuples import Book, Chapter
from sources.scraper import Scraper

TOC = "https://wanderinginn.com/table-of-contents/"


class WanderingInn(Scraper):
    @staticmethod
    def matches(url):
        return "wanderinginn" in url

    @staticmethod
    def get_chapter_links(book_num):
        page = requests.get(TOC).content
        tree = html.fromstring(page)
        sel = f"p:contains(\"Volume {book_num}\") + p a"
        anchors = tree.cssselect(sel)

        return [anchor.get("href") for anchor in anchors]

    @staticmethod
    def make_chapter(page):
        tree = html.fromstring(page)

        for comment in tree.xpath("//comment()"):
            # There are some HTML comments in 7.25 (search "There were…she counted.")
            # that break lxml's tostring method. We'll get rid of them here.
            parent = comment.getparent()
            if parent is not None:
                parent.remove(comment)

        title = tree.cssselect(".entry-title")[0].text

        paragraphs = tree.cssselect(".entry-content > *")
        paragraphs = [p for p in paragraphs if not p.text_content().isspace()]

        for p in paragraphs:
            spans = p.cssselect("span")
            [span.attrib.pop("style", None) for span in spans]

        last_node_text = paragraphs[-1].text_content()
        if "Previous Chapter" in last_node_text or "Next Chapter" in last_node_text:
            paragraphs = paragraphs[:-2]


        try:
            content = "".join(map(Scraper.elem_tostring, paragraphs))
            return Chapter(title=title, text=content)
        except Exception:
            print('here')


    def make_book(self, url):
        book_num = int(url.split("-")[1])
        chapter_links = WanderingInn.get_chapter_links(book_num)

        chapter_pages = web.download_async(chapter_links)
        chapters = list(map(WanderingInn.make_chapter, chapter_pages))

        meta = {"author": "pirateaba"}
        title = f"The Wandering Inn - Book {book_num}"

        return Book(title, title, "en-US", meta, chapters)
