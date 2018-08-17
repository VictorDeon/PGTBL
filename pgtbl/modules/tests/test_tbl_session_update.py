from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from modules.models import TBLSession

User = get_user_model()


class TBLSessionUpdateTestCase(TestCase):
    """
    Test to update a TBL session.
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
            'modules:update',
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
        User can not create a new TBL session without logged in.
        """

        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_update_tbl_session_by_teacher(self):
        """
        Test to update a tbl session by teacher.
        """

        data = {'title': "TBL session title updated", 'description': "TBL session description"}
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        sessions_url = reverse_lazy(
            'modules:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, sessions_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, data['title'])
        check_messages(
            self, response,
            tag='alert-success',
            content='TBL session updated successfully.'
        )

    def test_update_tbl_session_by_monitors(self):
        """
        Test to update a tbl session by monitors if monitor is a teacher.
        """

        data = {'title': "TBL session title updated", 'description': "TBL session description"}
        self.client.login(username=self.teacher_monitor.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        sessions_url = reverse_lazy(
            'modules:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, sessions_url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, data['title'])
        check_messages(
            self, response,
            tag='alert-success',
            content='TBL session updated successfully.'
        )

    def test_update_tbl_session_fail(self):
        """
        User can not update a tbl session with invalid fields.
        """

        data = {'title': ''}
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(
            response, 'form', 'title', _("This field is required.")
        )
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, 'TBL session title')

    def test_update_tbl_session_by_student_fail(self):
        """
        Student can not update a tbl session.
        """

        data = {'title': "TBL session title updated", 'description': "TBL session description"}
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, "TBL session title")
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_update_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not update a tbl session.
        """

        data = {'title': "TBL session title updated", 'description': "TBL session description"}
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, "TBL session title")
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_update_tbl_session_by_user_fail(self):
        """
        User that is not in the discipline can not update a tbl session.
        """

        data = {'title': "TBL session title updated", 'description': "TBL session description"}
        self.client.login(username=self.user.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, "TBL session title")
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
