from zipfile import ZipFile
from sources.worm import worm

from jinja2 import Environment, FileSystemLoader


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
            file_name = 'OEBPS/content/Chapter{0}.html'.format(i + 1)
            file.writestr(file_name, html)


def main():
    scraper = worm.Worm()
    book = scraper.make_book()
    write_epub(book, 'Worm - Wildbow.epub')


if __name__ == '__main__':
    main()
