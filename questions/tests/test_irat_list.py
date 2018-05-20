from django.core.urlresolvers import reverse_lazy
from core.roles import Teacher
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import (
    check_messages, user_factory
)
import datetime
from django.utils import timezone
import pytz
from model_mommy import mommy
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from questions.views_irat import (
    IRATDateUpdateView
)


User = get_user_model()


class ListIRATTestCase(TestCase):
    """
    Test to list question into IRAT test.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.teacher = user_factory(name='Ricardo')
        self.student = user_factory(name='Ana', is_teacher=False)
        self.students = user_factory(qtd=2, is_teacher=False)
        self.students.append(self.student)

        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Software Test',
            course='Engineering',
            password='12345',
            students=self.students
        )

        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title='TBL1',
            irat_datetime=timezone.localtime(timezone.now()),
            irat_weight=3,
            irat_duration=30 # 30 minutes
        )

        self.question = mommy.make(
            Question,
            session=self.session
        )

        self.irat = IRATSubmission.objects.create(
                user_id = self.teacher.id,
                session_id = self.session.id,
                question_id = self.question.id
        )


    def tearDown(self):
        """
        This method will run after any test.
        """
        TBLSession.objects.all().delete()
        Discipline.objects.all().delete()
        User.objects.all().delete()



    def test_redirect_to_login(self):
        """
        User can not see the irat test without logged in.
        """

        pass

    def test_irat_test_pagination(self):
        """
        Test to show question by pagination.
        """

        pass

    def test_users_can_see_the_irat_list(self):
        """
        User like students, monitors and teacher can see the irat test
        with not exercise questions and when the date of irat arrive.
        """

        pass

    def test_users_can_not_see_the_irat_test(self):
        """
        User like students and monitors can not see the irat test if the
        time is behind date/time of irat teste or time is after date/time
        of irat test with its duration.
        """

        pass

    def test_only_teacher_can_change_weight_and_time(self):
        """
        Only teacher can change the irat test weight and duration.
        """

        pass

    def test_only_teacher_can_change_date_and_time(self):
        """
        Only teacher can change date and time from irat test.
        """

        pass

    def test_date_and_time_not_can_be_blank(self):
        """
        The date and time of irat test not can be blank.
        """

        response = self.client.post(
                reverse_lazy(
                        'questions:irat-date',
                        kwargs = {'slug': self.teacher.id, 'pk': self.session.id }),
                        {'irat_datetime': ''}
                )

        self.assertEquals(response.status_code, 302)


    def test_date_and_time_need_to_be_bigger_than_today(self):
        """
        The date and time from irat test need to be bigger than the
        date and time from today.
        """

        yesterday = timezone.localtime(timezone.now()) - timezone.timedelta(1)

        response = self.client.post(
            reverse_lazy(
            'questions:irat-date',
            kwargs = {'slug': self.teacher.id, 'pk': self.session.id }),
            {'irat_datetime': yesterday}
        )

        self.assertEquals(response.status_code, 302)
