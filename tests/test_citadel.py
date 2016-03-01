from unittest import TestCase
from sources import citadel
import validators
from lxml import html
from web import web


class TestCitadel(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.links = list(citadel.generate_links())
        cls.pages = web.download_async(cls.links)
        cls.trees = [html.fromstring(page) for page in cls.pages]
        cls.titles = [citadel.extract_title(tree) for tree in cls.trees]

    def test_generate_links(self):
        self.assertGreater(len(self.links), 50, 'Not enough links!')
        self.assertEqual('https://unillustrated.wordpress.com/monster/', self.links[0])
        self.assertTrue(all(validators.url(link) for link in self.links))

    def test_titles(self):
        self.assertEqual('Monster', self.titles[0], 'First title is not correct')

        titles_to_check = (
            '002.0 Introductions',
            '017.2 Realization (April Fools)',
            '32.0 Bide'
        )

        for expected_title in titles_to_check:
            self.assertTrue(expected_title in self.titles,
                            '{0} is not in list of titles'.format(expected_title))

        for title in self.titles:
            self.assertIsInstance(title, str,
                                  'Title must be string - instead got {0}'.format(title))
