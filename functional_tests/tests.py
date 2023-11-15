from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


import time
import unittest

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """test of new visitor"""

    def setUp(self):
        """setup"""
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        """demontage"""
        self.browser.quit()

	    
    def wait_for_row_in_list_table(self, row_text):
       ''' wait string in table of list'''
       start_time = time.time()
       while True:
          try:
             table = self.browser.find_element(By.ID, 'id_list_table')
             rows = table.find_elements(By.TAG_NAME, 'tr')
             self.assertIn(row_text, [row.text for row in rows])
             return
          except (AssertionError, WebDriverException) as e:
             if time.time() - start_time > MAX_WAIT:
                raise e
             time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """test: can begin list and get it later"""
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        print(header_text)
        self.assertIn('To-Do', header_text)  
	
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
	    inputbox.getAttribute('placeholder'),
	    'Enter a to-do item'
	)
        inputbox.send_keys('Buy peacock feathers')

        # When she is pressing 'Enter', the page is updating and it contains element '1: Buy peacock feathers' as an element of table 
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She is entering 'Make a peacock's feathers box'
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys("Make a peacock's feathers box")
        inputbox.send_keys(Keys.ENTER)

        # Page is updating again and is showing both elements of list
        self.wait_for_row_in_list_table("2: Make a peacock's feathers box") 
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # Witg satisfy Edit went to sleep
    
    def test_multiple_can_start_list_at_different_urls(self):
       '''test: many of users can start lists with different urls'''
       # Edit starts a new list
       self.browser.get(self.live_server_url)
       inputbox = self.browser.find_element(By.ID, 'id_new_item')
       inputbox.send_keys("Buy peacock feathers")
       inputbox.send_keys(Keys.ENTER)
       self.wait_for_row_in_list_table('1: Buy peacock feathers')

       # She mentions that her list has a unique URL-adress
       edith_list_url = self.browser.current_url
       self.assertRegex(edith_list_url, '/lists/.+')

       # Now new user Francis visits a site
       
       # We use a new session of brower providing that any information form Edith could not come across through cookie data
       self.browser.quit()
       self.browser = webdriver.Firefox()

       # Francis visits a home page. There are no Edith's list
       self.browser.get(self.live_server.url)
       page_text = self.browser.find_element(By.TAG_NAME, 'body').text
       self.assertNotIn('Buy peacock feathers', page_text)
       self.assertNotIn("Make a peacock's feathers box")

       # Francis starts a new list entering a new element
       inputbox = self.browser.find_element(By.ID, 'id_new_item')
       inputbox.send_keys('Buy milk')
       inputbox.send_keys(Keys.ENTER)
       self.wait_for_row_in_list_table('1: Buy milk')

       # Francis gets a unique URL adress
       francis_list_url = self.browser.current_url
       self.assertRegex(francis_list_url, '/lists/.+')
       self.assertNotEqual(francis_list_url, edith_list_url)

       # Check again: There no Edith's list
       page_text = self.browser.find_element(By.TAG_NAME, 'body').text
       self.assertNotIn('Buy peacock feathers', page_text)
       self.assertIn('Buy milk', page_text)
       
       # With satisfy they both went to sleep


       self.fail('To end the test')
# assert 'To-Do' in browser.title, "Browser title was " + browser.title

if __name__ == "__main__":
    unittest.main(warnings='ignore')


# Удовлетворенная она снова ложиться спать


