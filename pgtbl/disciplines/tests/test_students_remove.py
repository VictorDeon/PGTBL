from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    check_messages, user_factory
)

User = get_user_model()


class StudentsRemoveTestCase(TestCase):
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
        self.students = user_factory(
            qtd=8,
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

    def test_remove_student_by_teacher_ok(self):
        """
        Test to remove specific student from discipline and open the
        discipline again.
        """

        self.client.login(
            username=self.teacher.username, password='test1234'
        )
        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertEqual(self.discipline.is_closed, True)
        response = self.remove_user(self.students[0].pk, redirect_url, 7, 2)
        check_messages(
            self, response,
            tag='alert-success',
            content='You have removed {0} from {1}'.format(
                self.students[0].get_short_name(),
                self.discipline.title
            )
        )
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.is_closed, False)

    def test_remove_monitor_by_teacher_ok(self):
        """
        Test to remove specific monitor from discipline.
        """

        self.client.login(
            username=self.teacher.username, password='test1234'
        )
        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertEqual(self.discipline.is_closed, True)
        response = self.remove_user(self.teachers[2].pk, redirect_url, 8, 1)
        check_messages(
            self, response,
            tag='alert-success',
            content='You have removed {0} from {1}'.format(
                self.teachers[2].get_short_name(),
                self.discipline.title
            )
        )
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.is_closed, True)

    def test_remove_yourself_from_discipline(self):
        """
        Test to remove yourself from discipline.
        """

        self.client.login(
            username=self.students[0].username, password='test1234'
        )
        redirect_url = reverse_lazy('accounts:profile')
        response = self.remove_user(self.students[0].pk, redirect_url, 7, 2)
        check_messages(
            self, response,
            tag='alert-success',
            content='You left the discipline {0}'.format(self.discipline.title)
        )

    def test_can_not_remove_user_from_discipline1(self):
        """
        Test can't remove another user is you are not teacher from discipline.
        """

        self.client.login(
            username=self.students[0].username, password='test1234'
        )
        redirect_url = reverse_lazy(
            'disciplines:students',
            kwargs={'slug': self.discipline.slug}
        )
        response = self.remove_user(self.students[1].pk, redirect_url, 8, 2)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You can't remove {0} from {1}".format(
                self.students[1].get_short_name(),
                self.discipline.title
            )
        )

    def remove_user(self, user_id, redirect_url, students, monitors):
        """
        Verify if user is removed from discipline.
        """

        url = reverse_lazy(
            'disciplines:remove-student',
            kwargs={
                'slug': self.discipline.slug,
                'pk': user_id
            }
        )
        self.assertEqual(self.discipline.students.count(), 8)
        self.assertEqual(self.discipline.monitors.count(), 2)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.discipline.students.count(), students)
        self.assertEqual(self.discipline.monitors.count(), monitors)
        return response

    def test_can_not_remove_user_from_discipline_if_not_logged(self):
        """
        Test can't remove user from discipline if teacher not logged.
        """

        url = reverse_lazy(
            'disciplines:remove-student',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.students[0].pk
            }
        )
        response = self.client.post(url, follow=True)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, url)
        self.assertRedirects(response, redirect_url)

    def test_can_not_access_discipline(self):
        """
        Test can't access discipline features if user is not in discipline.
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
