from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages, user_factory
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from disciplines.models import Discipline
from TBLSessions.models import TBLSession


User = get_user_model()


class ListExerciseTestCase(TestCase):
    """
    Test to list question into exercise.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='password'
        )

        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@teacher.com',
            password='password'
        )

        self.monitor = User.objects.create_user(
            username='monitor',
            email='monitor@monitor.com',
            password='password'
        )

        self.client = Client()

        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='DisciplineVV',
            course='Software Engineering',
            password='12345',
            is_closed=False,
            students_limit=10,
            monitors_limit=3,
            students=[self.user],
            monitors=[self.monitor],
            make_m2m=True
        )
        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="TBL1",
            description="First TBL Session",
            is_closed=False,
            make_m2m=True
        )

        self.question1 = mommy.make(
            Question,
            title="Question 1",
            session=self.session,
            level="Basic",
            topic="What is the result between the sum of 1 + 1?",
            is_exercise=True
        )
        self.alternative1 = mommy.make(
            Alternative,
            title="3",
            is_correct=False,
            question=self.question1
        )
        self.alternative2 = mommy.make(
            Alternative,
            title="2",
            is_correct=True,
            question=self.question1
        )
        self.alternative3 = mommy.make(
            Alternative,
            title="1",
            is_correct=False,
            question=self.question1
        )
        self.alternative4 = mommy.make(
            Alternative,
            title="0",
            is_correct=False,
            question=self.question1
        )

       # Question 2
        self.question2 = mommy.make(
            Question,
            title="Question 1",
            session=self.session,
            level="Basic",
            topic="What is the result between the sum of 2 + 1?",
            is_exercise=True
        )
        self.alternative5 = mommy.make(
            Alternative,
            title="3",
            is_correct=True,
            question=self.question2
        )
        self.alternative6 = mommy.make(
            Alternative,
            title="2",
            is_correct=False,
            question=self.question2
        )
        self.alternative7 = mommy.make(
            Alternative,
            title="1",
            is_correct=False,
            question=self.question2
        )
        self.alternative8 = mommy.make(
            Alternative,
            title="0",
            is_correct=False,
            question=self.question2
        )        

        self.url = reverse_lazy(
            'questions:list',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.id,
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        Discipline.objects.all().delete()
        TBLSession.objects.all().delete()

    def test_redirect_to_login(self):
        """
        User can not see the exercise list without logged in.
        """

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        login_url = reverse_lazy('accounts:login')
        redirects_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirects_url)

    def test_file_pagination(self):
        """
        Test to show question by pagination.
        """

        self.client.login(username="test", password="password")

        url = '/profile/{}/sessions/{}/questions/'.format(self.session.discipline.slug,self.session.id)
        response = self.client.get(url)

        paginator = response.context['paginator']

        # Total number of questions
        self.assertEqual(Question.objects.filter(session= self.session).count(),2)
        # Total number of questions, across all pages.
        self.assertEqual(paginator.count, 2)
        # The maximum number of quations to include on a page.
        self.assertEqual(paginator.per_page, 1)
        # Total number of pages.
        self.assertEqual(paginator.num_pages, 2)

    def test_users_can_see_the_exercise_list(self):
        """
        User like students, monitors and teacher can see the exercise list
        with exercise questions.
        """

        # Realize the login as student
        self.client.login(username="test", password="password")
        url = '/profile/{}/sessions/{}/questions/'.format(self.session.discipline.slug, self.session.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Get the question has been showed in the screen
        questions = Question.objects.filter(session= self.session).count()
        self.assertEqual(questions, 2)

        # Realize the login as monitor
        self.client.login(username="monitor", password="password")
        url = '/profile/{}/sessions/{}/questions/'.format(self.session.discipline.slug, self.session.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Get the question has been showed in the screen
        questions = Question.objects.filter(session= self.session).count()
        self.assertEqual(questions, 2)

        # Realize the login as teacher
        self.client.login(username="teacher", password="password")
        url = '/profile/{}/sessions/{}/questions/'.format(self.session.discipline.slug, self.session.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Get the question has been showed in the screen
        questions = Question.objects.filter(session= self.session).count()
        self.assertEqual(questions, 2)
