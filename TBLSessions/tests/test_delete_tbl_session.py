from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import Discipline
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

        self.student_monitor = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='someMonitorpass',
            is_teacher=False
        )

        self.monitor_and_teacher = User.objects.create_user(
            username='someMonitor2',
            email='monitor2Email@email.com',
            password='someMonitor2pass',
            is_teacher=False
        )

        self.student = User.objects.create_user(
            username='someStudent',
            email='studentEmail@email.com',
            password='someStudentpass',
            is_teacher=False            
        )

        self.discipline = mommy.make(
            Discipline,
            teacher=self.monitor_and_teacher,
            students= [ self.student, self.student_monitor ],
            monitors=[
                self.student_monitor, 
                self.monitor_and_teacher, 
                self.teacher
            ]
        )

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=1
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
        self.student_monitor.delete()
        self.student.delete()
        self.monitor_and_teacher.delete()

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
        self.assertEqual(TBLSession.objects.count(), 1)

        self.client.login(
            username=self.teacher.username, 
            password='someTeacherpass'
        )
        successful_response = self.client.post(self.url, follow=True)
        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': self.discipline.slug}
        )

        self.assertRedirects(successful_response, success_url)
        self.assertEqual(TBLSession.objects.count(), 0)
        check_messages(
            self, successful_response,
            tag='alert-success',
            content="TBL session deleted successfully."
        )

    def test_delete_tbl_session_by_monitors(self):
        """
        Test to delete a tbl session by monitors if they are a teacher.
        """
        self.assertEqual(TBLSession.objects.count(), 1)
        
        self.client.login(username=self.monitor_and_teacher.username, password='someMonitor2pass')
        successful_response = self.client.post(self.url, follow=True)
        success_url = reverse_lazy(
            'TBLSessions:list',
            kwargs={'slug': self.discipline.slug}
        )

        #self.assertRedirects(successful_response, success_url)
        self.assertEqual(TBLSession.objects.count(), 0)
        check_messages(
            self, successful_response,
            tag='alert-success',
            content="TBL session deleted successfully."
        )


    def test_delete_tbl_session_by_student_fail(self):
        """
        Student can not delete a tbl session.
        """
        self.assertEqual(TBLSession.objects.count(), 1)
        self.client.login(username=self.student.username, password='someStudentpass')

        unsuccessful_response = self.client.post(self.url, follow=True)
        profile_url = reverse_lazy('accounts:profile')

        self.assertRedirects(unsuccessful_response, profile_url)
        self.assertEqual(TBLSession.objects.count(), 1)
        check_messages(
            self, unsuccessful_response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_delete_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not delete a tbl session.
        """
        self.assertEqual(TBLSession.objects.count(), 1)
        self.client.login(username=self.student_monitor.username, password='someMonitorpass')
        
        unsuccessful_response = self.client.post(self.url, follow=True)
        profile_url = reverse_lazy('accounts:profile')

        self.assertRedirects(unsuccessful_response, profile_url)
        self.assertEqual(TBLSession.objects.count(), 1)
        check_messages(
            self, unsuccessful_response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )