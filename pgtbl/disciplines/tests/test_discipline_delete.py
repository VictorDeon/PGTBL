from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from core.test_utils import check_messages

User = get_user_model()


class DisciplineDeleteTestCase(TestCase):
    """
    Test to delete a disciplina.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='Test2',
            email='test2@gmail.com',
            password='test1234'
        )
        self.discipline = Discipline.objects.create(
            teacher=self.teacher,
            slug='discipline-1'
        )
        self.url = reverse_lazy(
            'disciplines:delete',
            kwargs={'slug': self.discipline.slug}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.discipline.delete()
        self.teacher.delete()

    def test_delete_discipline_ok(self):
        """
        Test to delete discipline with success.
        """

        self.assertEqual(Discipline.objects.count(), 1)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertEqual(Discipline.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Discipline deleted successfully."
        )

    def test_delete_another_teacher_discipline(self):
        """
        Try to delete a discipline from another teacher.
        """

        another_teacher = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='test1234',
            is_teacher=True
        )
        self.client.login(
            username=another_teacher.username,
            password='test1234'
        )
        self.assertEqual(Discipline.objects.count(), 1)
        response = self.client.post(self.url, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertEqual(Discipline.objects.count(), 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_delete_discipline_by_student(self):
        """
        Student try to delete a discipline.
        """

        self.assertEqual(Discipline.objects.count(), 1)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertEqual(Discipline.objects.count(), 1)
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
