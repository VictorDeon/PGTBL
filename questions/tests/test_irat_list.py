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
from django.template.defaultfilters import slugify

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
            slug='test',
            classroom='Class A',
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

        url = '/profile/{}-{}-{}/sessions/{}/irat/'.format(
                    self.discipline.id,
                    slugify(self.discipline.title),
                    slugify(self.discipline.classroom),
                    self.session.id
                )


        response = self.client.get(url, follow=True)

        self.assertRedirects(response, '/login/?next=' + url,
                             status_code=302)

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

        after_irat = timezone.localtime(timezone.now()) + timezone.timedelta(1)

        response = self.client.get(
                reverse_lazy(
                        'questions:irat-list',
                        kwargs = {'slug': self.student.id, 'pk': self.session.id }),
                        {'irat_datetime': after_irat}
                )

        self.assertEquals(response.status_code, 302)

    def test_only_teacher_can_change_weight_and_time(self):
        """
        Only teacher can change the irat test weight and duration.
        """

        # Simulates student trying to modify iRAT's weight and time
        self.client.login(username=self.student.username, password='test1234')
        
        data = {
            'irat_weight': 5,
            'irat_duration': 50,
        }

        url = reverse_lazy(
                'questions:irat-update',
                kwargs = {'slug': self.discipline.slug, 'pk': self.session.id}
        )

        response = self.client.post(url, data, follow=True)
        # failure_redirect_path = reverse_lazy(
        #         'TBLSessions:details',
        #         kwargs = {'slug': self.discipline.slug, 'pk': self.session.id }
        # )

        # self.assertRedirects(response, failure_redirect_path)
        self.session.refresh_from_db()
        
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

        # Simulates teacher triyng to modify iRAT's weight and time

        self.client.logout()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(url, data, follow=True)
        
        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs = {'slug': self.discipline.slug, 'pk': self.session.id }
        )

        self.assertRedirects(response, success_url)
        self.session.refresh_from_db()
        check_messages(
            self, response,
            tag='alert-success',
            content="iRAT updated successfully."
        )


    def test_only_teacher_can_change_date_and_time(self):
        """
        Only teacher can change date and time from irat test.
        """

        # Simulates student trying to modify iRAT's date
        self.client.login(username=self.student.username, password='test1234')
        
        data = {
            'irat_datetime':datetime.datetime(2019, 8, 7, 14),
        }

        url = reverse_lazy(
                'questions:irat-date',
                kwargs = {'slug': self.discipline.slug, 'pk': self.session.id}
        )

        response = self.client.post(url, data, follow=True)
        # failure_redirect_path = reverse_lazy(
        #         'TBLSessions:details',
        #         kwargs = {'slug': self.discipline.slug, 'pk': self.session.id }
        # )

        # self.assertRedirects(response, failure_redirect_path)
        self.session.refresh_from_db()
        
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

        # Simulates teacher triyng to modify iRAT's date

        self.client.logout()
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(url, data, follow=True)
        
        success_url = reverse_lazy(
            'questions:irat-list',
            kwargs = {'slug': self.discipline.slug, 'pk': self.session.id }
        )

        self.assertRedirects(response, success_url)
        self.session.refresh_from_db()
        self.assertEquals(response, 'oi')
        check_messages(
            self, response,
            tag='alert-success',
            content="iRAT updated successfully."
        )

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
