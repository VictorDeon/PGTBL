from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession

User = get_user_model()


class ShowPracticalTestCase(TestCase):
    """
    Test to show the practical test.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='teacherEmail@email.com',
            password='somepass'
            is_teacher=True
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.monitor.add(self.teacher)

        self.monitor = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='somepass'
            is_teacher=True
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.monitor.add(self.monitor)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )
        self.tbl_session = self.tbl_sessions[0]

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()
        self.monitor.delete()
        self.tbl_session.delete()

    def test_show_practical_test_to_student(self):
        """
        The practical test need to be opened by teacher for student to see
        """
        url = '/practical-test'

        successful_response = self.teacher.get(url, follow=True)
        self.assertEqual(successful_response.status_code, 200)        
        
    def test_teacher_and_monitor_can_see_practical_test(self):
        """
        Teacher and monitors that is a teacher can see the practical test,
        before it being opened.
        """
        url = '/practical-test'

        successful_response_teacher = self.teacher.get(url, follow=True)
        successful_response_monitor = self.teacher.get(url, follow=True)
        
        self.assertEqual(successful_response_teacher.status_code, 200)
        self.assertEqual(successful_response_monitor.status_code, 200)
        