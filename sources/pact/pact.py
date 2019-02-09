from sources.tuples import *
from sources.worm import Worm
from web import web

from .chapter_links import data


class Pact(Worm):
    def __init__(self):
        super().__init__()

        self.TITLE = "Pact"

        self.METADATA = {"author": "Wildbow"}

    @staticmethod
    def matches(url):
        return "pactwebserial.wordpress.com" in url

    def make_book(self, _):
        links = [d["link"] for d in data]
        titles = [d["title"] for d in data]

        pages = web.download_async(links)
        chapters = [
            self.make_chapter(title, page) for title, page in zip(titles, pages)
        ]

        return Book(self.TITLE, self.get_id(), self.LANGUAGE, self.METADATA, chapters)
