from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class HomePageViewTestCase(TestCase):
    """
    Test all the features of the home page.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()

    def test_status_code_200_ok(self):
        """
        Test the home page url status code.
        """

        response = self.client.get(reverse('core:home'))
        self.assertEquals(response.status_code, 200)

    def test_templates_used(self):
        """
        Test all templates used in this page.
        """

        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertTemplateUsed(response, 'core/navbar.html')
        self.assertTemplateUsed(response, 'home/parallax.html')
        self.assertTemplateUsed(response, 'home/features.html')
        self.assertTemplateUsed(response, 'news/news.html')
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertTemplateUsed(response, 'home/footer.html')
