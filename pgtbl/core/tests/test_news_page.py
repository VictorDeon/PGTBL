from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from core.models import News, Tag
from datetime import datetime


class NewsPageTestCase(TestCase):
    """
    Teste to show the news list page and details page.
    TODO:
        - search news
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()

        self.tag = Tag.objects.create(
            title='Importante',
            slug='importante'
        )

        self.news1 = News.objects.create(
            title='Noticia01',
            slug='noticia01',
            content='Primeira noticia.',
            created_at=datetime.now()
        )

        self.news2 = News.objects.create(
            title='Noticia02',
            slug='noticia02',
            content='Segunda noticia.',
            created_at=datetime.now(),
        )

        self.news3 = News.objects.create(
            title='Noticia03',
            slug='noticia03',
            content='Terceira noticia.',
            created_at=datetime.now(),
        )

        self.news2.tags.add(self.tag)
        self.news3.tags.add(self.tag)

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.news1.delete()
        self.news2.delete()

    def test_news_list_status_code_200_ok(self):
        """
        Test the news list page url status code.
        """

        response = self.client.get(reverse('core:news'))
        self.assertEquals(response.status_code, 200)

    def test_news_list_templates_used(self):
        """
        Test all templates used in this page.
        """

        response = self.client.get(reverse('core:news'))
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'news/list.html')

    def test_to_access_the_news_url_with_tag(self):
        """
        Test to access the news of a certain tag.
        """

        url = reverse('core:news-tag', kwargs={'tag': self.tag})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_filter_news_by_tag(self):
        """
        Test to filter news by tag.
        """

        self.assertEquals(News.objects.count(), 3)
        tag_news = News.objects.filter(tags=self.tag)
        self.assertEquals(tag_news.count(), 2)

    def test_news_details_status_code_200_ok(self):
        """
        Test the news details page url status code.
        """

        url = reverse('core:news-details', kwargs={'slug': self.news1.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_news_details_templates_used(self):
        """
        Test all templates used in this page.
        """

        url = reverse('core:news-details', kwargs={'slug': self.news1.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'news/details.html')
