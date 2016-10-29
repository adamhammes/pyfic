import time
import xml.etree.cElementTree as etree


class Scraper:
    def __init__(self):
        self.TITLE = 'DEFAULT'
        self.LANGUAGE = 'en-US'

        self.METADATA = {
            'author': 'DEFAULT',
        }

    @staticmethod
    def matches(url):
        raise NotImplementedError()

    @staticmethod
    def elem_tostring(elem):
        return etree.tostring(elem, encoding='unicode')

    def get_id(self):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        return '{0} {1}'.format(self.TITLE, time_str)

    def make_book(self):
        raise NotImplementedError()

