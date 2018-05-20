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

        pass

    def test_users_can_see_the_exercise_list(self):
        """
        User like students, monitors and teacher can see the exercise list
        with exercise questions.
        """

        pass
