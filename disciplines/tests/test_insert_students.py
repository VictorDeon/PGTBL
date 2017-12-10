from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    check_messages, user_factory
)

User = get_user_model()


class RemoveStudentsTestCase(TestCase):
    """
    Test to remove students or monitors from discipline.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.teachers = user_factory(qtd=4)
        self.student = user_factory(name='Maria', is_teacher=False)
        self.monitor = user_factory(name='Caio')
        self.students = user_factory(
            qtd=9,
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline04',
            course='Engineering',
            password='12345',
            is_closed=True,
            students_limit=10,
            monitors_limit=3,
            students=self.students,
            monitors=self.teachers[2:],
            make_m2m=True
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        User.objects.all().delete()

    def test_insert_student_by_teacher_ok(self):
        """
        Test teacher can insert student into discipline.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        redirect_url = reverse_lazy(
            'disciplines:users',
            kwargs={'slug': self.discipline.slug}
        )
        self.insert_student(
            self.student, 10, 2, redirect_url,
            tag='alert-success',
            msg='{0} was inserted in the discipline: {1}'.format(
                self.student.get_short_name(),
                self.discipline.title
            )
        )

    def test_insert_monitor_by_teacher(self):
        """
        Test teacher can add monitors into discipline.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        redirect_url = reverse_lazy(
            'disciplines:users',
            kwargs={'slug': self.discipline.slug}
        )
        self.insert_student(
            self.monitor, 9, 3, redirect_url,
            tag='alert-success',
            msg='{0} was inserted in the discipline: {1}'.format(
                self.monitor.get_short_name(),
                self.discipline.title
            )
        )

    def test_student_can_not_insert_student_into_discipline(self):
        """
        Test student can't insert student or monitor into discipline.
        """

        self.client.login(
            username=self.students[0].username,
            password='test1234'
        )
        redirect_url = reverse_lazy('accounts:profile')
        self.insert_student(
            self.student, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )
        self.insert_student(
            self.monitor, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )

    def test_teacher_can_not_insert_student_into_discipline(self):
        """
        Test teacher that not create the discipline
        can't insert student or monitor into discipline.
        """

        self.client.login(
            username=self.teachers[1].username,
            password='test1234'
        )
        redirect_url = reverse_lazy('accounts:profile')
        self.insert_student(
            self.student, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )
        self.insert_student(
            self.monitor, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )

    def test_student_that_not_in_discipline_can_not_insert_student(self):
        """
        Test students that are not in discipline can't
        insert student or monitor.
        """

        self.client.login(
            username=self.student.username,
            password='test1234'
        )
        redirect_url = reverse_lazy('accounts:profile')
        self.insert_student(
            self.student, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )
        self.insert_student(
            self.monitor, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )

    def test_teacher_that_not_in_discipline_can_not_insert_student(self):
        """
        Test teacher that are not in discipline as monitor can't
        insert student or monitor.
        """

        self.client.login(
            username=self.monitor.username,
            password='test1234'
        )
        redirect_url = reverse_lazy('accounts:profile')
        self.insert_student(
            self.student, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )
        self.insert_student(
            self.monitor, 9, 2, redirect_url,
            tag='alert-danger',
            msg='You are not authorized to do this action.'
        )

    def insert_student(self, user, students, monitors, redirect_url, tag, msg):
        """
        Insert student or monitor into discipline.
        """

        url = reverse_lazy(
            'disciplines:insert-students',
            kwargs={
                'slug': self.discipline.slug,
                'pk': user.id
            }
        )
        self.assertEqual(self.discipline.students.count(), 9)
        self.assertEqual(self.discipline.monitors.count(), 2)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.discipline.students.count(), students)
        self.assertEqual(self.discipline.monitors.count(), monitors)
        check_messages(
            self, response,
            tag=tag,
            content=msg
        )

    def test_can_not_insert_student_if_discipline_is_crowed(self):
        """
        Test can't insert student if discipline is crowed.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        redirect_url = reverse_lazy(
            'disciplines:users',
            kwargs={'slug': self.discipline.slug}
        )
        url = reverse_lazy(
            'disciplines:insert-students',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.student.id
            }
        )
        self.assertEqual(self.discipline.students.count(), 9)
        self.assertEqual(self.discipline.monitors.count(), 2)
        self.discipline.students.add(self.student)
        self.discipline.monitors.add(self.monitor)
        self.assertEqual(self.discipline.students.count(), 10)
        self.assertEqual(self.discipline.monitors.count(), 3)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.discipline.students.count(), 10)
        self.assertEqual(self.discipline.monitors.count(), 3)
        check_messages(
            self, response,
            tag='alert-danger',
            content="Crowded discipline."
        )

    def test_can_not_insert_monitor_if_discipline_is_crowed(self):
        """
        Test can't insert student if discipline is crowed.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        redirect_url = reverse_lazy(
            'disciplines:users',
            kwargs={'slug': self.discipline.slug}
        )
        url = reverse_lazy(
            'disciplines:insert-students',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.monitor.id
            }
        )
        self.assertEqual(self.discipline.students.count(), 9)
        self.assertEqual(self.discipline.monitors.count(), 2)
        self.discipline.students.add(self.student)
        self.discipline.monitors.add(self.monitor)
        self.assertEqual(self.discipline.students.count(), 10)
        self.assertEqual(self.discipline.monitors.count(), 3)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.discipline.students.count(), 10)
        self.assertEqual(self.discipline.monitors.count(), 3)
        check_messages(
            self, response,
            tag='alert-danger',
            content="There are no more vacancies to monitor"
        )

    def test_not_logged_teacher_can_not_insert_student(self):
        """
        Test teacher can't insert student into discipline if not logged.
        """

        url = reverse_lazy(
            'disciplines:insert-students',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.student.id
            }
        )
        response = self.client.post(url, follow=True)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, url)
        self.assertRedirects(response, redirect_url)
