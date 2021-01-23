from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class MainIndexViewTests(TestCase):
    def test_is_present(self):
        """
        Something responds at the index url
        """
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
