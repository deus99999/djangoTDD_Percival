from django.urls import resolve
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


class NewListTest(TestCase):
   def test_can_save_a_POST_request(self):
       '''test: can save post request'''
       self.client.post('/lists/new', data={'item_text': 'A new list item'})
       self.assertEqual(Item.objects.count(), 1)
       new_item = Item.objects.first()
       self.assertEqual(new_item.text, 'A new list item')

   def test_redirects_after_POST(self):
       '''test: redirects after post request'''
       response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
       
       # Вместо этого
       #self.assertEqual(response.status_code, 302)
       #self.assertEqual(response['location'], '/lists/list/')
       # Можно использовать это
       self.assertRedirects(response, '/lists/list/')



class ListViewTest(TestCase):
   '''test fot list viewing'''
   def test_displays_all_items(self):
      Item.objects.create(text='itemey 1')
      Item.objects.create(text='itemey 2')

      response = self.client.get('/lists/list/')
       
      self.assertContains(response, 'itemey 1')
      self.assertContains(response, 'itemey 2')

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
    


       #self.assertIn('A new list item', response.content.decode())
       #self.assertTemplateUsed(response, 'home.html')
    
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
