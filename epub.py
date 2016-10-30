from zipfile import ZipFile
from sources import Worm, Citadel, FanfictionDotNet
from jinja2 import Environment, FileSystemLoader
import sys
import time


def write_epub(book, title):
    env = Environment(loader=FileSystemLoader('templates'))
    with ZipFile(title, 'w') as file:
        file.write('templates/mimetype', 'mimetype')
        file.write('templates/container.xml', 'META-INF/container.xml')

        content_opf = env.get_template('content.jnj').render(book=book)
        file.writestr('OEBPS/content.opf', content_opf)

        tox_ncx = env.get_template('tox.jnj').render(book=book)
        file.writestr('OEBPS/toc.ncx', tox_ncx)

        for i, chapter in enumerate(book.chapters):
            html = env.get_template('xhtml.jnj').render(chapter=chapter)
            file_name = 'OEBPS/content/Chapter{}.html'.format(i + 1)
            file.writestr(file_name, html)


def get_matching_scraper(url):
    scrapers = [Worm(), Citadel(), FanfictionDotNet()]

    try:
        return next(s for s in scrapers if s.matches(url))
    except StopIteration:
        return None


def generate_file_name(book):
    return '{} - {}.epub'.format(book.title, book.meta['author'])

def make_book(url):
    scraper = get_matching_scraper(url)

    if not scraper:
        return

    book = scraper.make_book(url)
    write_epub(book, generate_file_name(book))
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
