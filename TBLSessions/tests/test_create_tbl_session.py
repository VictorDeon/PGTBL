from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession
from disciplines.models import Discipline

User = get_user_model()


class CreateTBLSessionTestCase(TestCase):
    """
    Test to create a new TBL session.
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

        #Student Monitor
        self.monitor = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='someMonitorpass',
            is_teacher=False
        )

        #Teacher Monitor
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

        #Creating discipline conected to the teacher
        self.discipline = mommy.make(Discipline, teacher=self.teacher)
        self.discipline.students.add(self.student)
        self.discipline.monitors.add(self.monitor, self.monitor_and_teacher)

        #URL
        self.url = reverse_lazy(
            'TBLSessions:create', kwargs={'slug' : self.discipline.slug})

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()

    def test_redirect_to_login(self):
        """
        User can not create a new TBL session without logged in.
        """

        self.assertEqual(TBLSession.objects.count(), 0)

        failed_response = self.client.post(self.url, follow=True)
        redirect_to = '/login/?next=/profile/{}/sessions/add/'.format(
            self.discipline.slug,
            self.id
        )

        self.assertRedirects(failed_response, redirect_to, 302)
        self.assertEqual(TBLSession.objects.count(), 0)

    def test_create_tbl_session_by_teacher(self):
        """
        Test to create a new tbl session by teacher.
        """

        data = {
            'title' : 'TBLTest',
            'description' : 'Teste description',
            'is_closed' : False
        }

        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='someTeacherpass')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TBLSession.objects.count(), 1)
        check_messages(
            self, response,
            tag = 'alert-success',
            content = 'TBL session created successfully.'
            )

    def test_create_tbl_session_by_monitors(self):
        """
        Test to create a new tbl session by monitors if monitor is a teacher.
        """

        data = {
            'title' : 'TBLTest',
            'description' : 'Teste description',
            'is_closed' : False
        }

        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.monitor_and_teacher.username, password='someMonitor2pass')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TBLSession.objects.count(), 1)
        check_messages(
            self, response,
            tag = 'alert-success',
            content = 'TBL session created successfully.'
            )        

    def test_create_tbl_session_fail(self):
        """
        User can not create a tbl session with invalid fields.
        """

        data = {
            'title' : '',
            'description' : '',
            'is_closed' : False
        }

        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='someTeacherpass')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(TBLSession.objects.count(), 0)

        check_messages(
            self, response,
            tag = 'alert-danger',
            content = 'Invalid fields, please fill in the fields correctly.'
            )

    def test_create_tbl_session_by_student_fail(self):
        """
        Student can not create a tbl session.
        """

        data = {
            'title' : 'TBLTest',
            'description' : 'Teste description',
            'is_closed' : False
        }

        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.student.username, password='someStudentpass')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TBLSession.objects.count(), 0)
        check_messages(
            self, response,
            tag = 'alert-danger',
            content = 'You are not authorized to do this action.'
            )

    def test_create_tbl_session_by_monitors_fail(self):
        """
        Student monitors can not create a tbl session.
        """

        data = {
            'title' : 'TBLTest',
            'description' : 'Teste description',
            'is_closed' : False
        }

        #Testing with student monitor
        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.monitor.username, password='someMonitorpass')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TBLSession.objects.count(), 0)
        check_messages(
            self, response,
            tag = 'alert-danger',
            content = 'You are not authorized to do this action.'
            )

        #Testing with monitor and teacher
        self.assertEqual(TBLSession.objects.count(), 0)
        self.client.login(username=self.monitor_and_teacher.username, password='someMonitor2pass')
        response = self.client.post(self.url, data, follow=True)
        profile_url = reverse_lazy('accounts:profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TBLSession.objects.count(), 1)
        check_messages(
            self, response,
            tag = 'alert-success',
            content = 'TBL session created successfully.'
            )
