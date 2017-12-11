from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    list_transform, check_messages, user_factory
)

User = get_user_model()


class ListDisciplineTestCase(TestCase):
    """
    Tests to view all students and monitors from discipline.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.student = user_factory(name='João', is_teacher=False)
        self.students = user_factory(qtd=10, is_teacher=False)
        self.monitors = user_factory(qtd=3)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            students_limit=10,
            monitors_limit=3,
            students=self.students,
            monitors=self.monitors,
            make_m2m=True
        )
        self.url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
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
        self.assertTemplateUsed(response, 'disciplines/students.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        response = self.client.get(self.url)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('students' in response.context)
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

    def test_discipline_students(self):
        """
        Test the discipline students quantity.
        """

        self.assertEqual(User.objects.count(), 15)
        self.assertEqual(self.discipline.students.count(), 10)
        self.assertEqual(self.discipline.monitors.count(), 3)

    def test_discipline_students_pagination(self):
        """
        Test to show discipline students pagination.
        """

        response = self.client.get(self.url)
        paginator = response.context['paginator']
        students = response.context['students']
        # Total number of objects, across all pages.
        self.assertEqual(paginator.count, 13)
        # The maximum number of items to include on a page.
        self.assertEqual(paginator.per_page, 12)
        # Total number of pages.
        self.assertEqual(paginator.num_pages, 2)
        # Number of discipline students in one page
        self.assertEqual(students.count(), 12)

    def test_page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        response = self.client.get('{0}?page=3'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_discipline_students_list(self):
        """
        Test to list discipline users.
        """

        response = self.client.get(self.url)
        context = response.context['students']
        users = (self.discipline.students.all() |
                 self.discipline.monitors.all())
        # Only 12 students are rendered in context, so it has to decrease 1 of
        # the users since they are 13
        self.assertEqual(
            context.count(),
            users.count() - 1
        )

    def test_filter_by_students(self):
        """
        Test to filter discipline students.
        """

        response = self.client.get('{0}?filter=students'.format(self.url))
        context = response.context['students']
        students = self.discipline.students.all()
        self.assertEqual(
            list_transform(context),
            list_transform(students)
        )

    def test_filter_by_monitors(self):
        """
        Test to filter discipline monitors.
        """

        response = self.client.get('{0}?filter=monitors'.format(self.url))
        context = response.context['students']
        monitors = self.discipline.monitors.all()
        self.assertEqual(
            list_transform(context),
            list_transform(monitors)
        )

    def test_can_not_access_discipline_students(self):
        """
        Test can't access discipline students features if user is not in
        discipline.
        """

        self.client.login(
            username=self.student.username, password='test1234'
        )
        url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.client.get(url, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
