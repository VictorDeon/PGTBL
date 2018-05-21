from django.core.urlresolvers import reverse_lazy
from django.shortcuts import reverse
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
        self.session = mommy.make('TBLSession')
        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='someTeacher@email.com',
            password='teacherpass123',
            is_teacher=True,
        )
        self.session.discipline.teacher = self.teacher
        self.session.discipline.save()

        self.student = User.objects.create_user(
            username='someStudent',
            email='someStudent@email.com',
            password='studentpass123',
        )
        self.session.discipline.students.add(self.student)

        self.monitor = User.objects.create_user(
            username='someMonitor',
            email='someMonitor@email.com',
            password='monitorpass123',
        )
        self.session.discipline.monitors.add(self.monitor)

        self.url = reverse('TBLSessions:practical-details',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()

    def test_show_practical_test_to_student(self):
        """
        The practical test need to be opened by teacher for student to see
        """

        self.client.login(
            username=self.student.username,
            password='studentpass123'
        )

        successful_response = self.client.get(self.url)
        self.assertEqual(successful_response.status_code, 302)        
        
    def test_teacher_can_see_practical_test(self):
        """
        Teacher can see the practical test,
        before it being opened.
        """
        
        self.client.login(
            username=self.teacher.username,
            password='teacherpass123'
        )
        
        successful_response = self.client.get(self.url)
        self.assertEqual(successful_response.status_code, 200)
    
    def test_monitor_can_see_practical_test(self):
        """
        Monitor can see the practical test,
        before it being opened.
        """
        
        self.client.login(
            username=self.monitor.username,
            password='monitorpass123'
        )
        
        successful_response = self.client.get(self.url)
        self.assertEqual(successful_response.status_code, 302)
    