from django.urls import resolve
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string


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
