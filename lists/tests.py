from django.urls import resolve
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.
class HomePageTest(TestCase):
    '''home page test'''

    def test_uses_home_template(self):
        '''test: uses home template'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_returns_correct_html(self):
        '''test: home page returns correct html'''
        # request = HttpRequest()
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))	

        self.assertTemplateUsed(response, 'home.html')
        # exexpected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>'.strip(), html)
        # self.assertTrue(html.strip().endswith('</html>'))
    
    def test_can_save_a_POST_request(self):
       '''test: can save post request'''
       response = self.client.post('/', data={'item_text': 'A new list item'})
       self.assertIn('A new list item', response.content.decode())
       self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    '''module element of list test'''
    def test_saving_and_retrieving_items(self):
       '''saving and retrieving elements of list'''
       first_item = Item()
       first_item.text = 'The first (ever) list item'
       first_item.save()

       second_item = Item()
       second_item.text = 'Item the second'
       second_item.save()
       
       saved_items = Item.objects.all()
       
       self.assertEqual(saved_items.count(), 2)
       
       first_saved_item = saved_items[0]
       second_saved_item = saved_items[1]
       self.assertEqual(first_saved_item.text, 'The first (ever) list item')
       self.assertEqual(second_saved_item.text, 'Item the second')
