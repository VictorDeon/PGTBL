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

        self.client = Client()
        self.teacher = user_factory(name='Pedro')
        self.teachers = user_factory(qtd=2)
        self.student = user_factory(name='Maria', is_teacher=False)
        self.monitor = user_factory(name='João')
        self.students = user_factory(
            qtd=9,
            is_teacher=False
        )
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='DisciplineVV',
            course='Software Engineering',
            password='12345',
            is_closed=False,
            students_limit=10,
            monitors_limit=3,
            students=self.students,
            monitors=self.teachers,
            make_m2m=True
        )
        self.session = mommy.make(
            TBLSession,
            title="TBL1",
            description="First TBL Session",
            is_closed=False,
            make_m2m=True
        )
        self.question = mommy.make(
            Question,
            title="Question 1",
            session=self.session,
            level="Basic",
            topic="What is the result between the sum of 1 + 1?",
            is_exercise=True
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


    def test_user_can_see_exercise_result(self):
        """
        User like student, teacher and monitors can see the result of exercise.
        """

        self.client.login(username="test", password="password")
        url = '/profile/{}/sessions/1/questions/exercises/result/'.format(self.session.discipline.slug)

        # response = self.client.get(url, follow=True)
        # redirect_url, status_code = response.redirect_chain[-1]
        #
        # self.assertEqual(status_code, 302)
        # self.assertEqual(redirect_url, '/profile/')
        #
        # if '<h1>Login</h1>' in str(response.content):
        #     is_logged = False
        # else:
        #     is_logged = True
        #
        # self.assertIs(is_logged, True)

        pass

    def test_show_only_exercise_question(self):
        """
        Show only exercise question that are into exercise list with his
        result.
        """

        pass

    def test_calcule_the_exercise_result(self):
        """
        Calcule the exercise result from exercise list.
        score that the user made, total of scores and grade of user.
        """

        pass

    def test_reset_exercise_list(self):
        """
        Remove all submissions from exercise list.
        """

        pass
