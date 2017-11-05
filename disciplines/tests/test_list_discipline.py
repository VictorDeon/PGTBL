from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    user_factory
)

User = get_user_model()


class SimpleReadProfileDisciplinesTestCase(TestCase):
    """
    Simple test to view all user disciplines
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory()
        self.url = reverse_lazy('accounts:profile')
        self.client.login(username=self.teacher.username, password='test1234')

    def tearDown(self):
        self.teacher.delete()

    def test_status_code_200(self):
        """
        Test status code and templates.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertTemplateUsed(response, 'disciplines/collapse.html')

    def test_redirect_to_login(self):
        """
        Try to acess profile without logged in.
        """

        self.client.logout()
        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

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


class ReadProfileDisciplinesTestCase(TestCase):
    """
    Test to view all user disciplines.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(
            username='Teacher1',
            email='teacher1@gmail.com',
            password='test1234'
        )
        self.teachers = user_factory(2)
        self.students = user_factory(8, is_teacher=False)
        mommy.make(
            Discipline,
            teacher=self.teacher,
            _quantity=6
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            students=self.students,
            monitors=self.teachers,
            make_m2m=True
        )
        self.url = reverse_lazy('accounts:profile')
        self.client.login(username=self.teacher.username, password='test1234')

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        User.objects.all().delete()


    def test_disciplines(self):
        """
        Test the discipline quantity.
        """

        self.assertEqual(Discipline.objects.count(), 7)
        self.assertEquals(Discipline.objects.filter(
            teacher=self.teacher
        ).count(), 7)
        self.assertEqual(self.discipline.students.count(), 8)
        self.assertEqual(self.discipline.monitors.count(), 2)

    def test_teacher_discipline_pagination(self):
        """
        Test to show teacher disciplines pagination.
        """

        response = self.client.get(self.url)
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 8)
        self.assertEqual(paginator.per_page, 6)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(disciplines.count(), 6)

    def page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        response = self.client.get('{0}?page=3'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_filter_created_disciplines_by_teacher(self):
        """
        Test to filter created disciplines by teacher.
        """

        response = self.client.get('{0}?filter=created'.format(self.url))
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 8)
        self.assertEqual(paginator.per_page, 6)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(disciplines.count(), 6)

    def test_filter_teacher_monitor_disciplines(self):
        """
        Test to filter disciplines that teacher is monitor.
        """

        response = self.client.get('{0}?filter=monitor'.format(self.url))
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 0)
        self.assertEqual(paginator.per_page, 6)
        self.assertEqual(paginator.num_pages, 1)
        self.assertEqual(disciplines.count(), 0)

    def test_all_student_disciplines(self):
        """
        Test to show students disciplines pagination.
        """

        self.client.logout()
        self.client.login(
            username=self.students[0].username, password='test1234'
        )
        response = self.client.get(self.url)
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 1)
        self.assertEqual(paginator.per_page, 6)
        self.assertEqual(paginator.num_pages, 1)
        self.assertEqual(disciplines.count(), 1)

    def test_filter_student_monitor_disciplines(self):
        """
        Test to filter disciplines that teacher is monitor.
        """

        self.client.logout()
        self.client.login(
            username=self.students[0].username, password='test1234'
        )
        response = self.client.get('{0}?filter=monitor'.format(self.url))
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 0)
        self.assertEqual(paginator.per_page, 6)
        self.assertEqual(paginator.num_pages, 1)
        self.assertEqual(disciplines.count(), 0)
