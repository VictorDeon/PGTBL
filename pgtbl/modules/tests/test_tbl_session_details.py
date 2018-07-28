from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession

User = get_user_model()


class DetailTBLSessionTestCase(TestCase):
    """
    Test to show the TBL session.
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
        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="TBL session title",
            description="TBL session description"
        )
        self.url = reverse_lazy(
            'modules:practical-details',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.pk
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.session.delete()

    def test_redirect_to_login(self):
        """
        User can not see tbl session details without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_status_code_200(self):
        """
        Test status code and templates.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/details.html')
        self.assertTemplateUsed(response, 'modules/sidebar.html')

    def test_context(self):
        """
        Test to get all context from page.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url)
        self.assertTrue('user' in response.context)
        self.assertTrue('discipline' in response.context)
        self.assertTrue('session' in response.context)
        self.assertTrue('irat_datetime' in response.context)
        self.assertTrue('grat_datetime' in response.context)
        self.assertTrue('date' in response.context)

    def test_student_can_access_tbl_session(self):
        """
        The TBL session need to be opened by teacher for student to see
        """

        self.client.login(username=self.student.username, password='test1234')
        self.session.is_closed = False
        self.session.save()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/details.html')

    def test_monitor_can_access_tbl_session(self):
        """
        The monitors can access TBL sessions without be opened
        """

        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/details.html')

    def test_monitor_teacher_can_see_tbl_sessions(self):
        """
        The monitors that is a teacher can access TBL sessions without be opened
        """

        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/details.html')

    def test_teacher_can_see_tbl_sessions(self):
        """
        Teacher can see the tbl sessions before it being opened.
        """

        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modules/details.html')

    def test_student_can_not_access_tbl_session(self):
        """
        The tbl session need to be opened by teacher for student to see
        """

        self.client.login(username=self.student.username, password='test1234')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )