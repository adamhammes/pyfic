from zipfile import ZipFile
from sources import Worm, Citadel, FanfictionDotNet, Pact
from jinja2 import Environment, FileSystemLoader
import sys
import time
import htmlmin


def render_minified(env, file_name, **args):
    unminified = env.get_template(file_name).render(args)
    return htmlmin.minify(unminified, remove_comments=True, reduce_boolean_attributes=True,
                          reduce_empty_attributes=True, remove_optional_attribute_quotes=True)


def write_epub(book, file_name):
    env = Environment(loader=FileSystemLoader('templates'))
    with ZipFile(file_name, 'w') as file:
        file.write('templates/mimetype', 'mimetype')
        file.write('templates/container.xml', 'META-INF/container.xml')

        content_opf = render_minified(env, 'content.jnj', book=book)
        file.writestr('OEBPS/content.opf', content_opf)

        tox_ncx = render_minified(env, 'tox.jnj', book=book)
        file.writestr('OEBPS/toc.ncx', tox_ncx)

        for i, chapter in enumerate(book.chapters):
            chapter_html = render_minified(env, 'xhtml.jnj', chapter=chapter)
            file_name = 'OEBPS/content/Chapter{}.html'.format(i + 1)
            file.writestr(file_name, chapter_html)

        if book.cover:
            image_path = 'OEBPS/content/cover-photo.jpg'
            file.writestr(image_path, book.cover)

            file.write('templates/cover.html', 'OEBPS/content/cover.html')


def get_matching_scraper(url):
    scrapers = [Worm(), Citadel(), FanfictionDotNet(), Pact()]

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
