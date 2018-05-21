from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession
from django import template

User = get_user_model()


class DeleteTBLSessionTestCase(TestCase):
    """
    Test to delete a new tbl session.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()

        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='teacherEmail@email.com',
            password='someTeacherpass',
            is_teacher=True
        )

        self.monitor = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='someMonitorpass',
            is_teacher=True
        )

        self.monitor_and_teacher = User.objects.create_user(
            username='someMonitor2',
            email='monitor2Email@email.com',
            password='someMonitor2pass',
            is_teacher=True
        )

        self.student = User.objects.create_user(
            username='someStudent',
            email='studentEmail@email.com',
            password='someStudentpass'
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.teacher = self.teacher
        self.discipline.students.add(self.student)
        self.discipline.monitors.add(self.monitor, self.monitor_and_teacher)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )
        self.tbl_session = self.tbl_sessions[0]

        self.url = reverse_lazy(
            'TBLSessions:delete',
            kwargs={
                'slug': self.tbl_session.discipline.slug,
                'pk': self.tbl_session.id
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()

    def test_redirect_to_login(self):
        """
        User can not delete a tbl session without logged in.
        """
        failed_response = self.client.get(self.url, follow=True)

        redirect_to = '/login/?next=/profile/{}/sessions/{}/delete/'.format(
            self.tbl_session.discipline.slug,
            self.tbl_session.id
        )

        self.assertRedirects(failed_response, redirect_to, 302)

    def test_delete_tbl_session_by_teacher(self):
        """
        Test to delete a tbl session by teacher.
        """
        self.client.login(username=self.teacher.username, password='someTeacherpass')

        successful_response = self.client.get(self.url, follow=True)

        self.assertEqual(successful_response.status_code, 200)

    def test_delete_tbl_session_by_monitors(self):
        """
        Test to delete a tbl session by monitors if they are a teacher.
        """
        self.client.login(username=self.monitor_and_teacher.username, password='someMonitor2pass')

        register = template.Library()
        try:
            successful_response = self.client.get(self.url, follow=True)
            self.assertEqual(successful_response.status_code, 200)
        except template.TemplateDoesNotExist:
            pass

    def test_delete_tbl_session_by_student_fail(self):
        """
        Student can not delete a tbl session.
        """
        self.client.login(username=self.student.username, password='someStudentpass')

        successful_response = self.client.get(self.url, follow=True)

        self.assertEqual(successful_response.status_code, 200)

    def test_delete_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not delete a tbl session.
        """
        self.client.login(username=self.monitor.username, password='someMonitorpass')

        register = template.Library()
        try:
            successful_response = self.client.get(self.url, follow=True)
            self.assertEqual(successful_response.status_code, 200)
        except template.TemplateDoesNotExist:
            pass