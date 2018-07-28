from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory
from disciplines.models import Discipline
from modules.models import TBLSession

User = get_user_model()


class TBLSessionListTestCase(TestCase):
    """
    Test to list tbl sessions.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.teacher_monitor = user_factory(name="otavio", is_teacher=True)
        self.student = user_factory(name="joao", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student],
            monitors=[self.monitor, self.teacher_monitor]
        )
        self.sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="TBL session title",
            description="TBL session description",
            _quantity=6
        )
        self.url = reverse_lazy(
            'modules:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.client.login(username=self.teacher.username, password='test1234')

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        TBLSession.objects.all().delete()

    def test_redirect_to_login(self):
        """
        User can not see the tbl session list without logged in.
        """

        self.client.logout()
        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_status_code_200(self):
        """
        Test status code and templates.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/list.html')
        self.assertTemplateUsed(response, 'modules/add.html')
        self.assertTemplateUsed(response, 'core/pagination.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        response = self.client.get(self.url)
        self.assertTrue('user' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('sessions' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('date' in response.context)

    def test_tbl_session_pagination(self):
        """
        Test to show tbl session by pagination.
        """

        response = self.client.get(self.url)
        paginator = response.context['paginator']
        sessions = response.context['sessions']
        self.assertEqual(paginator.count, 6)
        self.assertEqual(paginator.per_page, 5)
        self.assertEqual(paginator.num_pages, 2),
        self.assertEqual(sessions.count(), 5)

    def test_page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        response = self.client.get('{0}?page=3'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_users_can_see_the_tbl_sessions(self):
        """
        User like students, monitors and teacher can see the list of tbl
        sessions.
        """

        self.client.logout()
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_see_the_sessions(self):
        """
        User that is not in the discipline can not see the list of sessions.
        """

        self.client.logout()
        self.client.login(username=self.user.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
