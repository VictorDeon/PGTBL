from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
# from django.utils.timezone import timezone

from questions.views_grat import GRATResultView

User = get_user_model()


def setup_view(view, request, *args, **kwargs):
        """Mimic ``as_view()``, but returns view instance.
        Use this function to get view instances on which you can run unit tests,
        by testing specific methods."""

        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view


class GRATResultTestCase(TestCase):
    """
    Test to show grat test result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        # Preparing TBL Section
        self.client = Client()
        self.student = User.objects.create_user(
            username='estudante',
            email='estudante@email.com',
            password='estudante123'
        )

        self.tbl_session = mommy.make('TBLSession')
        self.tbl_session.discipline.students.add(self.student)


        self.question1 = mommy.make(
            Question,
            title = "Questão sobre a vida1",
            session = self.tbl_session,
            level = 'Basic',
            topic = "Whatever",
            is_exercise = True
        )

        self.question2 = mommy.make(
            Question,
            title = "Questão sobre a vida2",
            session = self.tbl_session,
            level = 'Basic',
            topic = "Whatever",
            is_exercise = False
        )


    def tearDown(self):
        """
        This method will run after any test.
        """
        self.student.delete()
        self.tbl_session.delete()



    def test_user_can_see_grat_result(self):
        """
        User like student, teacher and monitors can see the result of grat
        after the test is over or if student finish the test.
        """
        # /profile/materia/sessions/pk/grat/result
        url = '/profile/{}/sessions/{}/grat/result'.format(
            self.tbl_session.discipline.slug,
            self.tbl_session.pk
        )
        
        self.client.login(
            username=self.student.username,
            password='estudante123'
        )

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)



    def test_show_only_not_exercise_question(self):
        """
        Show only not exercise question that are into grat test, and show the
        answers.
        """

        # /profile/materia/sessions/pk/grat/result
        url = reverse_lazy(
            'questions:grat-result',
            kwargs = {
                'slug': self.tbl_session.discipline.slug,
                'pk': self.tbl_session.pk
            }
        )

        self.client.login(
            username=self.student.username,
            password='estudante123'
        )

        kawrgs = {'pk': self.tbl_session.pk }
        response = self.client.get(url, follow=True)

        view = setup_view(GRATResultView(), response, **kawrgs)
        questions = view.get_questions()

        self.assertEqual(questions[0], self.question2)
        


    def test_calcule_the_grat_result(self):
        """
        Calcule the grat test result from grat test.
        score that the group made, total of scores and grade of group.
        Only students have grade created.
        """
        pass
        
        

    def test_group_submit_test_only_once(self):
        """
        The student group can submit the test only once. Only one
        member of group need to submit the test.
        """

        pass

    def test_student_need_to_be_into_a_group(self):
        """
        User without group can not submit the test.
        """

        pass
