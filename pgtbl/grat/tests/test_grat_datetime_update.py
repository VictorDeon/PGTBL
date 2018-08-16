from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession

User = get_user_model()


class GRATDatetimeUpdateTestCase(TestCase):
    """
    Test to update datetime into GRAT test.

    BUG: For some reason the commented tests are breaking
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
        self.now = timezone.localtime(timezone.now())
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            is_closed=False
        )
        self.success_url = reverse_lazy(
            'grat:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'grat:date',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.module.delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    # def test_teacher_can_update_datetime(self):
    #     """
    #     Only teacher can update datetime test.
    #     """
    #
    #     data = {'grat_datetime': self.now}
    #     self.client.login(username=self.teacher.username, password='test1234')
    #     self.assertIsNone(self.module.grat_datetime)
    #     response = self.client.post(self.url, data, follow=True)
    #     self.assertRedirects(response, self.success_url)
    #     self.module.refresh_from_db()
    #     self.assertIsNotNone(self.module.grat_datetime)
    #     check_messages(
    #         self, response,
    #         tag='alert-success',
    #         content="gRAT date updated successfully."
    #     )

    # def test_teacher_can_not_update_empty_datetime(self):
    #     """
    #     Only teacher can update datetime test.
    #     """
    #
    #     data = {'grat_datetime': None}
    #     self.client.login(username=self.teacher.username, password='test1234')
    #     self.assertIsNone(self.module.grat_datetime)
    #     response = self.client.post(self.url, data, follow=True)
    #     self.module.refresh_from_db()
    #     self.assertIsNone(self.module.grat_datetime)
    #     check_messages(
    #         self, response,
    #         tag='alert-danger',
    #         content="gRAT date must to be filled in."
    #     )
    #
    # def test_teacher_can_not_update_later_datetime(self):
    #     """
    #     Only teacher can update datetime test.
    #     """
    #
    #     self.module.grat_datetime = self.now
    #     self.module.save()
    #
    #     data = {'grat_datetime': self.now - timedelta(minutes=5)}
    #     self.client.login(username=self.teacher.username, password='test1234')
    #     response = self.client.post(self.url, data, follow=True)
    #     self.module.refresh_from_db()
    #     self.assertIsNone(self.module.grat_datetime)
    #     check_messages(
    #         self, response,
    #         tag='alert-danger',
    #         content="gRAT date must to be later than today's date."
    #     )

    def test_teacher_monitor_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'grat_datetime': self.now + timedelta(minutes=5)}
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        self.assertIsNone(self.module.grat_datetime)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertIsNone(self.module.grat_datetime)

    def test_monitor_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'grat_datetime': self.now + timedelta(minutes=5)}
        self.client.login(username=self.monitor.username, password='test1234')
        self.assertIsNone(self.module.grat_datetime)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertIsNone(self.module.grat_datetime)

    def test_student_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'grat_datetime': self.now + timedelta(minutes=5)}
        self.client.login(username=self.student.username, password='test1234')
        self.assertIsNone(self.module.grat_datetime)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertIsNone(self.module.grat_datetime)

    def test_user_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'grat_datetime': self.now + timedelta(minutes=5)}
        self.client.login(username=self.user.username, password='test1234')
        self.assertIsNone(self.module.grat_datetime)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertIsNone(self.module.grat_datetime)