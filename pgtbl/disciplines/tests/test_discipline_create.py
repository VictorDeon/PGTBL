from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from core.test_utils import check_messages

User = get_user_model()


class DisciplineCreateTestCase(TestCase):
    """
    Test to create a new discipline by teacher.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234'
        )
        self.student = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234',
            is_teacher=False
        )
        self.url = reverse_lazy('disciplines:create')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.teacher.delete()
        self.student.delete()

    def test_create_discipline_ok(self):
        """
        Test to create a new discipline with success.
        """

        data = {
            'title': 'Discipline01',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'password': '12345',
            'students_limit': 60,
            'monitors_limit': 5
        }

        self.assertEqual(Discipline.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertEqual(Discipline.objects.count(), 1)
        check_messages(
            self, response,
            tag='alert-success',
            content="Discipline created successfully."
        )

    def test_create_discipline_input_fail(self):
        """
        Test to try create a discipline with invalid inputs.
        """

        data = {
            'title': '', 'description': '', 'classroom': '',
            'students_limit': 61, 'monitors_limit': 6
        }

        self.assertEqual(Discipline.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertFormError(
            response, 'form', 'title', _("This field is required.")
        )
        self.assertFormError(
            response, 'form', 'description', _("This field is required.")
        )
        self.assertFormError(
            response, 'form', 'classroom', _("This field is required.")
        )
        self.assertFormError(
            response, 'form', 'students_limit',
            _('There can be no more than 60 students in the class.')
        )
        self.assertFormError(
            response, 'form', 'monitors_limit',
            _('There can be no more than 5 monitors in the class.')
        )

        data = {
            'title': 'ok', 'description': 'ok', 'classroom': 'ok',
            'students_limit': 4, 'monitors_limit': 0
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Discipline.objects.count(), 0)
        self.assertFormError(
            response, 'form', 'students_limit',
            _('Must have at least 5 students in class.')
        )

    def test_create_discipline_by_student(self):
        """
        Student can't create a discipline.
        """

        self.assertEqual(Discipline.objects.count(), 0)
        self.client.login(username=self.student.username, password='test1234')
        data = {
            'title': 'Discipline01',
            'description': 'Discipline description.',
            'classroom': 'Class A',
            'password': '12345',
            'students_limit': 5,
            'monitors_limit': 0
        }
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertEqual(Discipline.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
