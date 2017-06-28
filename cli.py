from sources import *
from epub import epub
import sys
import time


def get_matching_scraper(url):
    scrapers = [Worm(), Citadel(), FanfictionDotNet(), Pact(), OrdersOfMagnitude(), Spacebattles()]

    try:
        return next(s for s in scrapers if s.matches(url))
    except StopIteration:
        return None


def make_book(url):
    scraper = get_matching_scraper(url)

    if not scraper:
        return

    book = scraper.make_book(url)
    epub.write_epub(book)
    return book


def main(args):
    url = args[0]

    start = time.clock()
    book = make_book(url)
    end = time.clock()

    if book:
        print('Downloaded "{}" in {:.2f} seconds.'.format(book.title, end - start))
    else:
        print('Could not find any matching scrapers.')


if __name__ == '__main__':
    main(sys.argv[1:])
