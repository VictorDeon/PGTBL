from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    list_transform, user_factory
)

User = get_user_model()


class DisciplineListTestCase(TestCase):
    """
    Tests to view all disciplines and search or filter discipline.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.teachers = user_factory(qtd=4)
        mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline',
            course='Course',
            _quantity=6
        )
        mommy.make(
            Discipline,
            teacher=self.teachers[0],
            title='Discipline01',
            course='Course01',
            _quantity=4
        )
        mommy.make(
            Discipline,
            teacher=self.teachers[1],
            title='Discipline02',
            course='Course02',
            is_closed=True,
            _quantity=2
        )
        self.url = reverse_lazy('disciplines:search')
        self.client.login(
            username=self.teacher.username, password='test1234'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        User.objects.all().delete()

    def test_status_code_200(self):
        """
        Test status code and templates.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'disciplines/list.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        response = self.client.get(self.url)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('disciplines' in response.context)
        self.assertTrue('date' in response.context)

    def test_redirect_to_login(self):
        """
        Try to acess profile without logged in.
        """

        self.client.logout()
        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_disciplines(self):
        """
        Test the discipline quantity.
        """

        # Total disciplines
        self.assertEqual(Discipline.objects.count(), 12)
        # Teacher disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teacher).count(), 6
        )
        # Teacher 0 disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teachers[0]).count(), 4
        )
        # Teacher 1 disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teachers[1]).count(), 2
        )

    def test_discipline_pagination(self):
        """
        Test to show disciplines pagination.
        """

        response = self.client.get(self.url)
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        # Total number of objects, across all pages.
        self.assertEqual(paginator.count, 6)
        # The maximum number of items to include on a page.
        self.assertEqual(paginator.per_page, 10)
        # Total number of pages.
        self.assertEqual(paginator.num_pages, 1)
        # Number of disciplines opened
        self.assertEqual(disciplines.count(), 6)

    def test_page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        response = self.client.get('{0}?page=2'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_order_by_course(self):
        """
        Test to order disciplines by course.
        """

        response = self.client.get('{0}?order=course'.format(self.url))
        disciplines = response.context['disciplines']
        ordered = Discipline.objects.available(
            user=self.teacher
        ).order_by('course')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(ordered)
        )

    def test_order_by_discipline_title(self):
        """
        Test to order disciplines by title.
        """

        response = self.client.get('{0}?order=title'.format(self.url))
        disciplines = response.context['disciplines']
        ordered = Discipline.objects.available(
            user=self.teacher
        ).order_by('title')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(ordered)
        )

    def test_order_by_teacher(self):
        """
        Test to order disciplines by teacher.
        """

        response = self.client.get('{0}?order=teacher__name'.format(self.url))
        disciplines = response.context['disciplines']
        ordered = Discipline.objects.available(
            user=self.teacher
        ).order_by('teacher__name')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(ordered)
        )

    def test_to_search_discipline(self):
        """
        Search a specific discipline.
        """

        response = self.client.get('{0}?q_info=Discipline02'.format(self.url))
        disciplines = response.context['disciplines']
        self.assertEqual(disciplines.count(), 2)
        searched = Discipline.objects.search('Discipline02')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(searched)
        )
