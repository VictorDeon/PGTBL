from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import (
    check_messages, user_factory
)
from core.roles import Teacher
from model_mommy import mommy
from questions.views_irat import (
    IRATResultView
)
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from django.utils import timezone
import pytz
from disciplines.models import Discipline
from TBLSessions.models import TBLSession

User = get_user_model()


class IRATResultTestCase(TestCase):
    """
    Test to show irat test result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = User.objects.create()

        self.discipline = Discipline.objects.create(
                title = 'Test',
                teacher_id = self.teacher.id
        )

        self.session = TBLSession.objects.create(
                discipline_id = self.discipline.id,
        )

        self.question = Question.objects.create(
                session_id = self.session.id
        )

        self.irat = IRATResultView()

    def tearDown(self):
        """
        This method will run after any test.
        """
        TBLSession.objects.all().delete()
        Discipline.objects.all().delete()
        User.objects.all().delete()
        IRATSubmission.objects.all().delete()

    def test_user_can_see_irat_result(self):

        """
        User like student, teacher and monitors can see the result of irat
        after the test is over or if student finish the test.
        """

        pass

    def test_show_only_not_exercise_question(self):
        """
        Show only not exercise question that are into irat test, and show the
        answers.
        """
        teacher_test = user_factory(name='Wallacy',password='passwordtest',is_teacher=True)


        discipline_test = mommy.make(
                Discipline,
                teacher = teacher_test,
                title='Calculus 2',
                course='Math',
                password='1234',
                classroom='Class C'
        )


        session_test = mommy.make(
                TBLSession,
                discipline=discipline_test,
                title='TBL4',
                irat_datetime=timezone.localtime(timezone.now()),
                irat_weight=3,
                irat_duration=30
        )

        exercise1 = mommy.make(Question,session=session_test,is_exercise=True)

        exercise2 = mommy.make(Question,session=session_test,is_exercise=True)

        exercise3 = mommy.make(Question,session=session_test,is_exercise=True)

        question1 = mommy.make(Question,session=session_test,is_exercise=False)

        question2 = mommy.make(Question,session=session_test,is_exercise=False)

        question3 = mommy.make(Question,session=session_test,is_exercise=False)

        self.client.login(username=teacher_test.username, password='passwordtest')

        question_list = [question1,question2,question3]
        exercise_list = [exercise1,exercise2,exercise3]


        url = '/profile/{}/sessions/{}/irat/'.format(session_test.discipline.slug, session_test.id)

        response = self.client.get(url)

        p = response.context['view'].get_queryset()

        query_list = list(p)

        for question in question_list:
            self.assertEquals(question in query_list,True)

        for exercise in exercise_list:
            self.assertEquals(exercise in query_list,False)



    def test_calcule_the_irat_result(self):

        """
        Calcule the irat test result from irat test.
        score that the user made, total of scores and grade of user.
        Only students have grade created.
        """

        pass
