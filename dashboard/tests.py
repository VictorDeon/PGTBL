from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from model_mommy import mommy
from django.core.urlresolvers import reverse_lazy
from disciplines.models import Discipline
from groups.models import Group
from TBLSessions.models import TBLSession
from grades.models import Grade, FinalGrade

User = get_user_model()

class DashboardTestModel(TestCase):


    def setUp(self):
        """
        This metho will run before any test case.
        """

        self.client = Client()
        self.teacher = User.objects.create_user(
            username='professor',
            email='test1@gmail.com',
            password='teacher1'
        )
        self.student = User.objects.create_user(
            username='Test3',
            email='test3@gmail.com',
            password='student1',
            is_teacher=False
        )
        self.student2 = User.objects.create_user(
            username='Test4',
            email='test4@gmail.com',
            password='student2',
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Discipline',
            course='Engineering',
            password='discipline1',
            students_limit=5,
            students=[self.student],
            make_m2m=True
        )
        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title='Test Session',
            description='Session for test',
            make_m2m=True
        )
        self.group = mommy.make(
            Group,
            discipline=self.discipline,
            title='Grupo Teste',
            students_limit=5,
            students=[self.student],
        )
        self.url = reverse_lazy(
            'dashboard:list',
            kwargs={'slug': self.discipline.slug, 'pk': self.session.id}
        )


    def tearDown(self):
        """
        This method will run after any test.
        """

        self.teacher.delete()
        self.student.delete()
        self.session.delete()
        self.group.delete()

    def test_student_can_see_dashboard(self):


        self.client.logout()
        self.client.login(
            username=self.student.username, password='student1'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile', response.url)

    def test_teacher_can_see_dashboard(self):


        self.client.logout()
        self.client.login(
            username=self.teacher.username, password='teacher1'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/list.html')
