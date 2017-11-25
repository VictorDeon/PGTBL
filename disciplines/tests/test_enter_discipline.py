from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    check_messages, list_transform, user_factory
)

User = get_user_model()


class SimpleSearchAndEnterDisciplineTestCase(TestCase):
    """
    Simple test to view all user disciplines, search and enter in discipline.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory()
        self.url = reverse_lazy('disciplines:search')
        self.client.login(username=self.teacher.username, password='test1234')

    def tearDown(self):
        self.teacher.delete()

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


class SearchAndEnterDisciplineTestCase(TestCase):
    """
    Test to view all user disciplines, search and enter in discipline.
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
        self.enter_url = reverse_lazy(
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

    def test_disciplines(self):
        """
        Test the discipline quantity.
        """

        # Total students
        self.assertEqual(
            User.objects.filter(is_teacher=False).count(), 12
        )
        # Total teachers
        self.assertEqual(
            User.objects.filter(is_teacher=True).count(), 5
        )
        # Total disciplines
        self.assertEqual(Discipline.objects.count(), 13)
        # Teacher disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teacher).count(), 7
        )
        # Teacher 0 disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teachers[0]).count(), 4
        )
        # Teacher 1 disciplines
        self.assertEquals(
            Discipline.objects.filter(teacher=self.teachers[1]).count(), 2
        )
        # Students and monitors in discipline
        self.assertEqual(self.discipline.students.count(), 8)
        self.assertEqual(self.discipline.monitors.count(), 2)

    def test_discipline_pagination(self):
        """
        Test to show disciplines pagination.
        """

        response = self.client.get(self.url)
        paginator = response.context['paginator']
        disciplines = response.context['disciplines']
        self.assertEqual(paginator.count, 4)
        self.assertEqual(paginator.per_page, 10)
        self.assertEqual(paginator.num_pages, 1)
        self.assertEqual(disciplines.count(), 4)

    def test_page_not_found(self):
        """
        Test to verify one page that not exists.
        """

        response = self.client.get('{0}?page=4'.format(self.url))
        self.assertEqual(response.status_code, 404)

    def test_order_by_course(self):
        """
        Test to order disciplines by course.
        """

        response = self.client.get('{0}?order=course'.format(self.url))
        disciplines = response.context['disciplines']
        ordered = Discipline.objects.available(user=self.teacher).order_by('course')
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
        ordered = Discipline.objects.available(user=self.teacher).order_by('title')
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
        ordered = Discipline.objects.available(user=self.teacher).order_by('teacher__name')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(ordered)
        )

    def test_to_search_discipline(self):
        """
        Search a specific discipline.
        """

        response = self.client.get('{0}?q_info=Discipline04'.format(self.url))
        disciplines = response.context['disciplines']
        self.assertEqual(disciplines.count(), 1)
        searched = Discipline.objects.search('Discipline04')
        self.assertEqual(
            list_transform(disciplines),
            list_transform(searched)
        )

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
        response = self.client.post(self.enter_url, password, follow=True)
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
        response = self.client.post(self.enter_url, password, follow=True)
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
        response = self.client.post(self.enter_url, password, follow=True)
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
        response = self.client.post(self.enter_url, password, follow=True)
        self.assertEqual(self.discipline.monitors.count(), 2)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Incorrect Password.'
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
        response = self.client.post(self.enter_url, password, follow=True)
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
        response = self.client.post(self.enter_url, password, follow=True)
        self.assertEqual(self.discipline.students.count(), 8)
        check_messages(
            self, response,
            tag='alert-danger',
            content='Incorrect Password.'
        )

    def test_only_teacher_can_close_discipline(self):
        """
        Only teacher can close your own discipline.
        """

        self.client.logout()
        self.client.login(
            username=self.teachers[2].username, password='test1234'
        )
        self.assertEqual(self.discipline.is_closed, False)
        url = reverse_lazy(
            'disciplines:close',
            kwargs={'slug': self.discipline.slug}
        )
        self.client.post(url, follow=True)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.is_closed, False)

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
        response = self.client.post(self.enter_url, password, follow=True)
        self.assertEqual(self.discipline.monitors.count(), 3)
        check_messages(
            self, response,
            tag='alert-danger',
            content='There are no more vacancies to monitor'
        )

    def test_can_not_access_discipline(self):
        """
        Test can't access discipline features if user is not in discipline.
        """

        self.client.login(
            username=self.student.username, password='test1234'
        )
        url = reverse_lazy(
            'disciplines:details',
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
