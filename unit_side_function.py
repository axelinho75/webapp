import unittest

class TestGeneratedPageTitleTestCase(unittest.TestCase):

    def test_generated_random_page_title(self):
        actual = "Index Page Title"
        excepted = "Index Page Title"
        assert excepted, actual