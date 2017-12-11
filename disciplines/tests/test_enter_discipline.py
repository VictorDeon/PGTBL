from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    check_messages, user_factory
)

User = get_user_model()


class EnterDisciplineTestCase(TestCase):
    """
    Tests to enter in discipline.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.teachers = user_factory(qtd=4)
        self.student = user_factory(
            name='Maria',
            username='maria',
            email='maria',
            is_teacher=False
        )
        self.students1 = user_factory(
            qtd=8,
            is_teacher=False
        )
        self.students2 = user_factory(
            qtd=3,
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            students_limit=10,
            monitors_limit=3,
            students=self.students1,
            monitors=self.teachers[2:],
            make_m2m=True
        )
        self.url = reverse_lazy(
            'disciplines:enter',
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

    def test_student_enter_discipline(self):
        """
        Test to student enter discipline with successfully.
        """

        self.client.logout()
        self.client.login(
            username=self.student.username, password='test1234'
        )
        self.assertEqual(self.discipline.students.count(), 8)
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.students.count(), 9)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        check_messages(
            self, response,
            tag='alert-success',
            content='You have been entered into the discipline: {0}'
            .format(self.discipline.title)
        )

    def test_enter_with_incorrect_password(self):
        """
        Test to enter with incorrect password to get into discipline.
        """

        self.client.logout()
        self.client.login(
            username=self.student.username, password='test1234'
        )
        self.assertEqual(self.discipline.students.count(), 8)
        password = {'password': '123'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.students.count(), 8)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Incorrect Password.'
        )

    def test_teacher_enter_discipline(self):
        """
        Test to teacher enter discipline as monitor with successfully.
        """

        self.client.logout()
        self.client.login(
            username=self.teachers[0].username, password='test1234'
        )
        self.assertEqual(self.discipline.monitors.count(), 2)
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.monitors.count(), 3)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        check_messages(
            self, response,
            tag='alert-success',
            content='You have been entered into the discipline: {0}'
            .format(self.discipline.title)
        )

    def test_teacher_enter_your_own_discipline(self):
        """
        Test teacher can't enter into your own disciplines.
        """

        self.assertEqual(self.discipline.monitors.count(), 2)
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.monitors.count(), 2)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't get into your own discipline."
        )

    def teste_to_enter_in_crowded_discipline(self):
        """
        Test student can't get into crowded disciplines because it's closed.
        """

        self.client.logout()
        self.client.login(
            username=self.student.username, password='test1234'
        )
        self.assertEqual(self.discipline.is_closed, False)
        self.discipline.students.add(self.students2[0])
        self.discipline.students.add(self.students2[1])
        self.assertEqual(self.discipline.students.count(), 10)
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.students.count(), 10)
        self.discipline.refresh_from_db()
        self.assertTrue(self.discipline.is_closed)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Crowded discipline.'
        )

    def test_user_can_not_enter_closed_disciplines(self):
        """
        Test that ensures that the discipline is closed and no one can
        enter it.
        """

        self.assertEqual(self.discipline.is_closed, False)
        self.assertEqual(self.discipline.students.count(), 8)
        url = reverse_lazy(
            'disciplines:close',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.client.post(url, follow=True)
        self.discipline.refresh_from_db()
        self.assertTrue(self.discipline.is_closed)
        self.assertEqual(self.discipline.students.count(), 8)
        self.client.logout()
        self.client.login(
            username=self.student.username, password='test1234'
        )
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.students.count(), 8)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Discipline is closed.'
        )

    def test_no_vacancies_monitor_discipline(self):
        """
        Test teacher can't get into disciplines as monitor.
        """

        self.client.logout()
        self.client.login(
            username=self.teachers[1].username, password='test1234'
        )
        self.discipline.monitors.add(self.teachers[0])
        self.assertEqual(self.discipline.monitors.count(), 3)
        password = {'password': '12345'}
        response = self.client.post(self.url, password, follow=True)
        self.assertEqual(self.discipline.monitors.count(), 3)
        check_messages(
            self, response,
            tag='alert-danger',
            content='There are no more vacancies to monitor'
        )
