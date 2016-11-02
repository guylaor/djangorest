from django.test import TestCase, Client
from shorty.models import ShortUrl
from django.core.exceptions import ValidationError


class TestUrlModels(TestCase):

    def test_str_representation(self):
        ShortUrl.objects.all().delete()
        url = ShortUrl()
        url.default_url = 'http://google.com'
        url.save()
        u = ShortUrl.objects.get(default_url='http://google.com')
        self.assertEqual(str(u), 'Short Url:3e9 Default Url:http://google.com')

    def test_invalid_url_returns_error(self):
        with self.assertRaises(Exception) as context:
            ShortUrl.objects.all().delete()
            u = ShortUrl()
            u.default_url = 'http://googl'
            u.save()
            self.assertTrue('This is broken' in context.exception)
        self.assertEqual(ShortUrl.objects.all().count(), 0)


class TestApiMethods(TestCase):

    def setUp(self):
        url = ShortUrl()
        url.default_url = 'http://bbc.com'
        url.mobile_url = 'http://m.bbc.com'
        url.tablet_url = 'http://t.bbc.com'
        url.save()
        url = ShortUrl()
        url.default_url = 'http://google.com'
        url.save()

    def test_api_get_all_urls(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('/api/urls/')
        # print(response.content)
        self.assertContains(response, 'http://bbc.com')
        self.assertContains(response, 'http://m.bbc.com')
        self.assertContains(response, 'http://t.bbc.com')
        self.assertContains(response, 'http://google.com')

    def test_redirect_to_mobile_url(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X)')
        response = c.get('/3e9')
        self.assertRedirects(response, 'http://m.bbc.com', fetch_redirect_response=False)

    def test_redirect_to_tablet_url(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0 (iPad; CPU iPhone OS 5_0 like Mac OS X)')
        response = c.get('/3e9')
        self.assertRedirects(response, 'http://t.bbc.com', fetch_redirect_response=False)

    def test_redirect_to_desktop_url(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('/3e9')
        self.assertRedirects(response, 'http://bbc.com', fetch_redirect_response=False)

    def test_redirect_to_default_url(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0 (iPad; CPU iPhone OS 5_0 like Mac OS X)')
        response = c.get('/3ea')
        self.assertRedirects(response, 'http://google.com', fetch_redirect_response=False)

    def test_api_post_saves_new_url(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.post('/api/urls/', {'default_url': 'http://mtv.com'})
        self.assertEqual(response.status_code, 201)   # response code for created
        response = c.get('/api/urls/')
        self.assertContains(response, 'http://mtv.com')
