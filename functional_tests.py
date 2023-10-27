from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    """test of new visitor"""

    def setUp(self):
        """setup"""
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        """demontage"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """can begin list and get it later"""
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('To end the test')

# assert 'To-Do' in browser.title, "Browser title was " + browser.title

if __name__ == "__main__":
    unittest.main(warnings='ignore')


# Удовлетворенная она снова ложиться спать

