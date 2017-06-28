from zipfile import ZipFile
from jinja2 import Environment, FileSystemLoader


def render_template(env, file_name, **args):
    return env.get_template(file_name).render(args)


def write_epub(book):
    env = Environment(loader=FileSystemLoader('epub'))
    file_name = generate_file_name(book)

    with ZipFile(file_name, 'w') as file:
        file.write('epub/mimetype', 'mimetype')
        file.write('epub/container.xml', 'META-INF/container.xml')

        content_opf = render_template(env, 'content.jnj', book=book)
        file.writestr('OEBPS/content.opf', content_opf)

        tox_ncx = render_template(env, 'tox.jnj', book=book)
        file.writestr('OEBPS/toc.ncx', tox_ncx)

        for i, chapter in enumerate(book.chapters):
            chapter_html = render_template(env, 'xhtml.jnj', chapter=chapter)
            file_name = 'OEBPS/content/Chapter{}.html'.format(i + 1)
            file.writestr(file_name, chapter_html)

        if book.cover:
            image_path = 'OEBPS/content/cover-photo.jpg'
            file.writestr(image_path, book.cover)

            file.write('epub/cover.html', 'OEBPS/content/cover.html')


def generate_file_name(book):
    return '{} - {}.epub'.format(book.title, book.meta['author'])
