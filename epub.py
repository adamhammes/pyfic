from zipfile import ZipFile
from sources import citadel
from jinja2 import Environment, FileSystemLoader


def main(env):
    book = citadel.make_book()
    with ZipFile('citadel.epub', 'w') as file:
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

if __name__ == '__main__':
    environment = Environment(loader=FileSystemLoader('templates'))
    main(environment)
