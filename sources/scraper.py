import time
import os
import xml.etree.cElementTree as etree


class Scraper:
    def __init__(self):
        self.TITLE = "DEFAULT"
        self.LANGUAGE = "en-US"

        self.METADATA = {"author": "DEFAULT"}

    @staticmethod
    def matches(url):
        raise NotImplementedError()

    @staticmethod
    def elem_tostring(elem):
        return etree.tostring(elem, encoding="unicode")

    @staticmethod
    def get_relative_path(path):
        """
        A nasty hack to get a path relative to the working directory (even on Windows). See
        http://stackoverflow.com/questions/4060221/
        """
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        return os.path.join(location, path)

    def get_id(self):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        return "{} {}".format(self.TITLE, time_str)

    def make_book(self, url):
        raise NotImplementedError()
