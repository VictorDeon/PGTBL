from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from irat.forms import IRATForm
from modules.models import TBLSession

User = get_user_model()


class IRATUpdateTestCase(TestCase):
    """
    Test to update IRAT test.

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
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test",
            is_closed=False
        )
        self.failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.success_url = reverse_lazy(
            'irat:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )
        self.url = reverse_lazy(
            'irat:update',
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

    # def test_teacher_can_update_irat(self):
    #     """
    #     Only teacher can update iRAT test.
    #     """
    #
    #     data = {
    #         'irat_weigth': 5,
    #         'irat_duration': 10
    #     }
    #     self.client.login(username=self.teacher.username, password='test1234')
    #     self.assertEqual(self.module.irat_weight, 3)
    #     self.assertEqual(self.module.irat_duration, 30)
    #     response = self.client.post(self.url, data, follow=True)
    #     self.assertRedirects(response, self.success_url)
    #     self.module.refresh_from_db()
    #     self.assertEqual(self.module.irat_weight, 5)
    #     self.assertEqual(self.module.irat_duration, 10)
    #     check_messages(
    #         self, response,
    #         tag='alert-success',
    #         content="iRAT updated successfully."
    #     )

    def test_teacher_monitor_can_not_update_irat(self):
        """
        Only teacher can update iRAT test.
        """

        data = {'irat_weigth': 5, 'irat_duration': 10}
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)

    def test_monitor_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'irat_weigth': 5, 'irat_duration': 10}
        self.client.login(username=self.monitor.username, password='test1234')
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)

    def test_student_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'irat_weigth': 5, 'irat_duration': 10}
        self.client.login(username=self.student.username, password='test1234')
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)

    def test_user_can_not_update_datetime(self):
        """
        Only teacher can update datetime test.
        """

        data = {'irat_weigth': 5, 'irat_duration': 10}
        self.client.login(username=self.user.username, password='test1234')
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)
        self.client.post(self.url, data, follow=True)
        self.module.refresh_from_db()
        self.assertEqual(self.module.irat_weight, 3)
        self.assertEqual(self.module.irat_duration, 30)