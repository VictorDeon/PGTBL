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
from questions.models import Question
from questions.models import Submission


User = get_user_model()


class ExerciseResultTestCase(TestCase):
    """
    Test to show exercise result.
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
            is_correct=True,
            question=self.question1
        )
        self.alternative2 = mommy.make(
            Alternative,
            title="2",
            is_correct=False,
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
        self.submission = mommy.make(
            Submission,
            session=self.session,
            question=self.question1,
            user=self.user,
            correct_alternative=self.alternative2
        )

        self.question2 = mommy.make(
            Question,
            title="Question 2",
            session=self.session,
            level="Basic",
            topic="What is the result between the sum of 1 and 1?",
            is_exercise=False
        )
        self.alternative21 = mommy.make(
            Alternative,
            title="3",
            is_correct=False,
            question=self.question2
        )
        self.alternative22 = mommy.make(
            Alternative,
            title="2",
            is_correct=True,
            question=self.question2
        )
        self.alternative23 = mommy.make(
            Alternative,
            title="1",
            is_correct=False,
            question=self.question2
        )
        self.alternative24 = mommy.make(
            Alternative,
            title="0",
            is_correct=False,
            question=self.question2
        )

        self.submission = mommy.make(
            Submission,
            session=self.session,
            question=self.question1,
            user=self.user,
            correct_alternative=self.alternative2
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
        Question.objects.all().delete()
        Submission.objects.all().delete()
        Alternative.objects.all().delete()


    def test_user_can_see_exercise_result(self):
        """
        User like student, teacher and monitors can see the result of exercise.
        """

        # Tests with the user being a student
        self.client.login(username="test", password="password")
        url = '/profile/{}/sessions/{}/exercises/result/'.format(self.session.discipline.slug, self.session.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Tests with the user being a teacher
        self.client.login(username="teacher", password="password")
        url = '/profile/{}/sessions/{}/exercises/result/'.format(self.session.discipline.slug, self.session.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Tests with the user being a monitor
        self.client.login(username="monitor", password="password")
        url = '/profile/{}/sessions/{}/exercises/result/'.format(self.session.discipline.slug, self.session.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_show_only_exercise_question(self):
        """
        Show only exercise question that are into exercise list with his
        result.
        """

        self.client.login(username="test", password="password")
        url = '/profile/{}/sessions/{}/exercises/result/'.format(self.session.discipline.slug, self.session.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Get only the questions that belongs to the exercise list
        questions = response.context['view'].get_questions()
        self.assertEqual(questions.count(), 1)

    def test_calcule_the_exercise_result(self):
        """
        Calcule the exercise result from exercise list.
        score that the user made, total of scores and grade of user.
        """

        self.client.login(username="test", password="password")

        response = self.client.get(self.url)

        page_obj = response.context['page_obj']

        url_answer = '/profile/{}/sessions/{}/exercises/question/{}/answer-page/{}/'.format(self.session.discipline.slug, self.session.id, self.question1.id, page_obj.number)

        data = {'alternative01-score':0,
                'alternative02-score':0,
                'alternative03-score':0,
                'alternative04-score':4
                }

        response = self.client.post(url_answer, data)

        url = '/profile/{}/sessions/{}/exercises/result/'.format(self.session.discipline.slug, self.session.id)
        response = self.client.get(url)

        content = '<span class=\"text-danger\">10.00</span>'
        self.assertTrue(content in str(response.content))

    def test_reset_exercise_list(self):
        """
        Remove all submissions from exercise list.
        """

        # Login of teacher user
        self.client.login(username="teacher", password="password")

        # Remove the question 1
        self.client.post('/profile/{}/sessions/{}/questions/{}/delete/'.format(self.session.discipline.slug, self.session.id, self.question1.id), params=None)

        # Remove the question 2
        self.client.post('/profile/{}/sessions/{}/questions/{}/delete/'.format(self.session.discipline.slug, self.session.id, self.question2.id), params=None)

        # Exercise list url
        url = '/profile/{}/sessions/{}/questions/'.format(self.session.discipline.slug, self.session.id)

        # Acess the url
        response = self.client.get(url, follow=True)

        # Testing if the page is returning status code 200
        self.assertEqual(response.status_code, 200)
        
        # Testing if there isn't questions in the page
        content = '<p>There is no questions in this session.</p>'
        self.assertTrue(content in str(response.content))

        # Testing if there is no Submissions and Question in the database
        self.assertEqual(Submission.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)
