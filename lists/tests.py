from django.urls import resolve
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest


# Create your tests here.
class HomePageTest(TestCase):
    '''home page test'''

    def test_root_url_resolves_to_home_page_view(self):
        '''test: root url to view of home page'''
        found = resolve('/')        
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''test: home page returns correct html'''
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
