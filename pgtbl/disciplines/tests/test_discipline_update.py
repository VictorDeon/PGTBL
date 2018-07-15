from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from core.test_utils import check_messages

User = get_user_model()


class DisciplineUpdateTestCase(TestCase):
    """
    Test to update discipline by teacher.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher1 = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234'
        )
        self.teacher2 = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234'
        )
        self.student = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='test1234',
            is_teacher=False
        )
        self.discipline = Discipline.objects.create(
            title='Discipline01',
            description='Discipline description.',
            classroom='Class A',
            students_limit=59,
            monitors_limit=5,
            is_closed=True,
            teacher=self.teacher1,
            slug='discipline01'
        )
        self.url = reverse_lazy(
            'disciplines:update',
            kwargs={'slug': self.discipline.slug}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.teacher1.delete()
        self.teacher2.delete()
        self.student.delete()
        self.discipline.delete()

    def test_update_discipline_ok(self):
        """
        Update the discipline by teacher successfully.
        """

        self.client.login(username=self.teacher1.username, password='test1234')
        data = {
            'title': 'Discipline modified',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'students_limit': 60,
            'monitors_limit': 5,
        }
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.title, 'Discipline modified')
        check_messages(
            self, response,
            tag='alert-success',
            content='Discipline updated successfully.'
        )

    def test_update_discipline_input_error(self):
        """
        Test to edit discipline without fields.
        """

        self.client.login(username=self.teacher1.username, password='test1234')
        data = {
            'title': '',
            'description': '',
            'classroom': '',
            'students_limit': 60,
            'monitors_limit': 5,
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(
            response, 'form', 'title', _("This field is required.")
        )
        self.assertFormError(
            response, 'form', 'description', _("This field is required.")
        )
        self.assertFormError(
            response, 'form', 'classroom', _("This field is required.")
        )
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.title, 'Discipline01')
        self.assertEqual(self.discipline.description, 'Discipline description.')
        self.assertEqual(self.discipline.classroom, 'Class A')

    def test_student_update_discipline(self):
        """
        Test to update discipline by student without success.
        """

        self.client.login(username=self.student.username, password='test1234')
        data = {
            'title': 'Discipline modified',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'students_limit': 60,
            'monitors_limit': 5,
        }
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.title, 'Discipline01')
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_another_teacher_update_discipline(self):
        """
        Test specific teacher can't update disciplines created by another
        teacher.
        """

        self.client.login(username=self.teacher2.username, password='test1234')
        data = {
            'title': 'Discipline modified',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'students_limit': 60,
            'monitors_limit': 5,
        }
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.title, 'Discipline01')
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_open_discipline_if_modify_students_limit(self):
        """
        If discipline is closed, open it if modify students limit.
        """

        self.client.login(username=self.teacher1.username, password='test1234')
        self.assertEqual(self.discipline.is_closed, True)
        data = {
            'title': 'Discipline modified',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'students_limit': 60,
            'monitors_limit': 5,
        }
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.title, 'Discipline modified')
        self.assertEqual(self.discipline.is_closed, False)
        check_messages(
            self, response,
            tag='alert-success',
            content='Discipline updated successfully.'
        )
