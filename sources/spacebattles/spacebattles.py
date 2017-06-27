"""
A module for screen scraping stories found on spacebattles.com
"""
import requests
from lxml import html, sax
from sources.tuples import Book, Chapter
from sources.scraper import Scraper
from web import web

FORUM_URL = 'https://forums.spacebattles.com/threads/'


class Spacebattles(Scraper):
    @staticmethod
    def matches(url):
        return 'spacebattles.com' in url

    @staticmethod
    def generate_links(story_id):
        """Returns [(title, url)]"""
        threadmark = FORUM_URL + story_id + '/threadmarks?category_id=1'
        page = requests.get(threadmark).content
        tree = html.fromstring(page)

        base = 'https://forums.spacebattles.com/'
        anchors = tree.cssselect('.threadmarkListItem a')
        return [(a.text.strip(), base + a.get('href')) for a in anchors]

    @staticmethod
    def fetch_post(url, page):
        tree = html.fromstring(page)
        if '#' in url:
            post_id = url.split('#')[1]
            return tree.cssselect('#{}'.format(post_id))[0]
        else:
            return tree.cssselect('.message')[0]

    @staticmethod
    def _generate_paragraph(contents):
        sink = sax.ElementTreeContentHandler()
        sink.startElementNS((None, 'p'), 'p')

        for child in contents:
            if isinstance(child, html.HtmlElement):
                sink.startElementNS((None, child.tag), child.tag)

                if child.text:
                    sink.characters(child.text)

                sink.endElementNS((None, child.tag), child.tag)
            else:
                sink.characters(child)

        sink.endElementNS((None, 'p'), 'p')
        return sink.etree.getroot()

    @staticmethod
    def _extract_content(post):
        message = post.cssselect('.messageContent blockquote')[0]
        text_nodes = message.xpath('child::node()')

        cleaned_nodes = []
        current_paragraph = []
        for node in text_nodes:
            if not isinstance(node, html.HtmlElement):
                current_paragraph.append(node.replace('\\n', '').replace('\\t', ''))
            elif node.tag == 'br':
                cleaned_nodes.append(Spacebattles._generate_paragraph(current_paragraph))
                current_paragraph.clear()
            else:
                current_paragraph.append(node)

        if current_paragraph:
            cleaned_nodes.append(Spacebattles._generate_paragraph(current_paragraph))

        return ''.join(map(Scraper.elem_tostring, cleaned_nodes))

    @staticmethod
    def make_chapter(url, page, title):
        post = Spacebattles.fetch_post(url, page)
        content = Spacebattles._extract_content(post)
        return Chapter(title, content)

    @staticmethod
    def make_chapters(story_id):
        chapter_infos = Spacebattles.generate_links(story_id)
        urls = [info[1] for info in chapter_infos]
        pages = web.download_async(urls)

        chapters = []
        for info, page in zip(chapter_infos, pages):
            title, url = info
            chapters.append(Spacebattles.make_chapter(url, page, title))

        return chapters

    @staticmethod
    def _get_story_id(url):
        relevant_bit = url[len(FORUM_URL):]
        return relevant_bit.split('/')[0]

    @staticmethod
    def _get_author(tree):
        return tree.cssselect('.username')[0].text

    @staticmethod
    def _get_title(tree):
        page_title = tree.cssselect('title')[0].text
        return page_title.rstrip(' | Spacebattles Forums')

    def make_book(self, url):
        story_id = Spacebattles._get_story_id(url)

        original_url = FORUM_URL + story_id
        page = requests.get(original_url).content
        tree = html.fromstring(page)

        self.TITLE = Spacebattles._get_title(tree)
        chapters = Spacebattles.make_chapters(story_id)
        meta = {'author': Spacebattles._get_author(tree)}

        return Book(self.TITLE, self.get_id(), 'en-US', meta, chapters)
