from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
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
        """test: can begin list and get it later"""
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        print(header_text)
        self.assertIn('To-Do', header_text)  
	
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
	    inputbox.get_attribute('placeholder'),
	    'Enter a to-do item'
	)
        inputbox.send_keys('Buy peacock feathers')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
	
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_element(By.NAME, 'tr')
        self.assertTrue(
		any(row.text == '1: Buy peacock feathers' for row in rows),
		'new element did not appear in list '
		)


        self.fail('To end the test')

# assert 'To-Do' in browser.title, "Browser title was " + browser.title

if __name__ == "__main__":
    unittest.main(warnings='ignore')


# Удовлетворенная она снова ложиться спать


