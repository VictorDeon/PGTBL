from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from disciplines.models import Discipline
from model_mommy import mommy
from core.test_utils import (
    check_messages, user_factory
)

User = get_user_model()


class DisciplineDetailTestCase(TestCase):
    """
    Tests to view disciplines details.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.other_teacher = user_factory(name='Mario')
        self.student = user_factory(
            name='Maria',
            username='maria',
            email='maria',
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
            make_m2m=True
        )
        self.url = reverse_lazy('disciplines:details')
        self.client.login(
            username=self.teacher.username, password='test1234'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        Discipline.objects.all().delete()
        User.objects.all().delete()

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

    def test_only_teacher_can_close_discipline(self):
        """
        Only teacher can close your own discipline.
        """

        self.client.logout()
        self.client.login(
            username=self.other_teacher.username, password='test1234'
        )
        self.assertEqual(self.discipline.is_closed, False)
        url = reverse_lazy(
            'disciplines:close',
            kwargs={'slug': self.discipline.slug}
        )
        self.client.post(url, follow=True)
        self.discipline.refresh_from_db()
        self.assertEqual(self.discipline.is_closed, False)
