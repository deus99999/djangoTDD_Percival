from django.urls import resolve
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


class NewItemTest(TestCase):
   def test_can_save_a_POST_request_to_an_existing_list(self):
       other_list = List.objects.create()
       correct_list = List.objects.create()

       self.client.post(
           f'/lists/{correct_list.id}/add_item',
           data={'item_text': 'A new item for an existing list'}
	)

       self.assertEqual(Item.objects.count(), 1)
       new_item = Item.objects.first()
       self.assertEqual(new_item.text, 'A new item for an existing list')
       self.assertEqual(new_item.list, correct_list)

   def test_redirects_to_list_view(self):
       other_list = List.objects.create()
       correct_list = List.objects.create()

       response = self.client.post(
           f'/lists/{correct_list.id}/add_item',
           data={'item_text': 'A new item for an existing list'}
        )

       self.assertRedirects(response, f'/lists/{correct_list.id}/')



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
       new_list = List.objects.first()

       # Вместо этого
       #self.assertEqual(response.status_code, 302)
       #self.assertEqual(response['location'], '/lists/list/')
       # Можно использовать это
       self.assertRedirects(response, f'/lists/{new_list.id}/')



class ListViewTest(TestCase):
   '''test fot list viewing'''
   def test_uses_list_template(self):
      '''test: using template of list'''
      list_ = List.objects.create()
      response = self.client.get(f'/lists/{list_.id}/')
      self.assertTemplateUsed(response, 'list.html')

   def test_displays_only_items_for_that_list(self):
      correct_list = List.objects.create()
      Item.objects.create(text='itemey 1', list=correct_list)
      Item.objects.create(text='itemey 2', list=correct_list)
      other_list = List.objects.create()
      Item.objects.create(text='other element of 1 list', list=other_list)
      Item.objects.create(text='other element of 2 list', list=other_list)

      response = self.client.get(f'/lists/{correct_list.id}/')
       
      self.assertContains(response, 'itemey 1')
      self.assertContains(response, 'itemey 2')
      self.assertNotContains(response, 'second element of 1 list')
      self.assertNotContains(response, 'second element of 2 list')

   def test_passes_correct_list_to_template(self):
      '''test: passes correct list to template'''
      other_list = List.objects.create()
      correct_list = List.objects.create()
      response = self.client.get(f'/lists/{correct_list.id}/')

      self.assertEqual(response.context['list'], correct_list)


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
        # print(html)
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
    
class ListAndItemModelTest(TestCase):
    '''module element of list test'''
    def test_saving_and_retrieving_items(self):
       '''saving and retrieving elements of list'''
       list_ = List()
       list_.save()

       first_item = Item()
       first_item.text = 'The first (ever) list item'
       first_item.list = list_
       first_item.save()

       second_item = Item()
       second_item.text = 'Item the second'
       second_item.list = list_
       second_item.save()
       
       saved_list = List.objects.first()
       self.assertEqual(saved_list, list_)

       saved_items = Item.objects.all()
       self.assertEqual(saved_items.count(), 2)
       
       first_saved_item = saved_items[0]
       second_saved_item = saved_items[1]
       self.assertEqual(first_saved_item.text, 'The first (ever) list item')
       self.assertEqual(first_saved_item.list, list_)
       self.assertEqual(second_saved_item.text, 'Item the second')
       self.assertEqual(second_saved_item.list, list_)
