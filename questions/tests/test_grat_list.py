from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from django.utils import timezone
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
import datetime
from django.template.defaultfilters import slugify
from groups.models import Group
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)
from questions.views_grat import (
    GRATDateUpdateView
)

User = get_user_model()


class ListGRATTestCase(TestCase):
    """
    Test to list question into GRAT test.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.student = User.objects.create_user(
            username='migue',
            email='migue@email.com',
            password='1234test'
        )

        self.teacher = User.objects.create_user(
            username='ajax',
            email='ajax@email.com',
            password='1234test'
        )

        self.monitor = User.objects.create_user(
            username='monitor',
            email='monitor@email.com',
            password='1234test'
        )

        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title='Teste de Software',
            course='Engenharia de Software',
            password='12345',
            classroom='Class A',
            slug='test',
            students=[self.student],
            monitors=[self.monitor]
        )

        self.session = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title='TBL1',
            grat_datetime=timezone.localtime(timezone.now()),
            grat_weight=3,
            grat_duration=30
        )

        self.groups = mommy.make(
            Group,
            discipline=self.discipline,
            title='Group 1',
            students_limit=4,
            students=[self.student]
        )

        self.question = mommy.make(
            Question,
            session=self.session
        )

        self.grat = mommy.make(
            GRATSubmission,
            group = self.groups
        )


        self.url = reverse_lazy(
            'questions:grat',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.session.id,
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()
        self.student.delete()
        self.session.delete()


    def test_redirect_to_login(self):
        """
        User can not see the grat test without logged in.
        """
        url = '/profile/{}/sessions/{}/grat/'.format(
            self.session.discipline.slug,
            self.session.id
        )

        response = self.client.get(url, follow=True)

        self.assertRedirects(response, '/login/?next=' + url,
                             status_code=302)


    def test_grat_test_pagination(self):
        """
        Test to show question by pagination.
        """

        pass


    def test_users_can_see_the_grat_list(self):
        """
        User like students, monitors and teacher can see the grat test
        with not exercise questions and when the date of grat arrive.
        """
        # Test with the user being student
        url = '/profile/{}/sessions/{}/grat'.format(
            self.session.discipline.slug,
            self.session.id
        )
        self.client.login(
            username=self.student.username,
            password=self.student.password
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

        # Test with the user being monitor
        url = '/profile/{}/sessions/{}/grat'.format(
            self.session.discipline.slug,
            self.session.id
        )
        self.client.login(
            username=self.monitor.username,
            password=self.monitor.password
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

        # Test with the user being teacher
        url = '/profile/{}/sessions/{}/grat'.format(
            self.session.discipline.slug,
            self.session.id
        )
        self.client.login(
            username=self.teacher.username,
            password=self.teacher.password
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)



    def test_users_can_not_see_the_grat_test(self):
        """
        User like students and monitors can not see the grat test if the
        time is behind date/time of grat teste or time is after date/time
        of grat test with its duration.
        """
        # Test with the user being student
        self.client.login(
            username=self.teacher.username,
            password=self.teacher.password
        )

        url = '/profile/{}/sessions/{}/grat/'.format(
            self.session.discipline.slug,
            self.session.id
        )

        response = self.session.grat_datetime = "2018-05-06T11:59"

        self.client.logout()

        self.client.login(
            username=self.student.username,
            password=self.student.password
        )

        response = self.client.get(url, follow=True)

        url_redirect = '/profile/{}/sessions/{}/details/'.format(
            self.session.discipline.slug,
            self.session.id
        )

        self.assertRedirects(response, '/login/?next=' + url_redirect, status_code=302)
        

    def test_only_teacher_can_change_weight_and_time(self):
        """
        Only teacher can change the grat test weight and duration.
        """
        url = '/profile/{}/sessions/{}/grat/edit-date'.format(
            self.session.discipline.slug,
            self.session.id
        )
        self.client.login(
            username=self.teacher.username,
            password=self.teacher.password
        )

        data = {
            'grat_datetime': datetime.datetime(2020, 12, 25, 4, 20),
        }

        response = self.client.post(self.url, data, follow=True)

        success_redirect_path = reverse_lazy (
            'TBLSession:details',
            kwargs = {
                'slug': self.discipline.slug,
                'pk': self.session.id
            }
        )
        self.assertEqual(success_redirect_path, "teste")
        self.assertRedirects(response, success_redirect_path)
        self.session.refresh_from_db()
        self.client.logout()

        self.assertEqual(self.session.datatime, datetime.datetime(2020, 12, 25, 4, 20))

        check_messages(
            self,
            response,
            tag='alert-success',
            content='gRAT date updated successfully.'
        )

    def test_only_teacher_can_change_date_and_time(self):
        """
        Only teacher can change date and time from grat test.
        """
        url = '/profile/{}/sessions/{}/grat/edit-date'.format(
            self.session.discipline.slug,
            self.session.pk
        )

        self.question = Question.objects.create(
            title='test',
            session=self.session,
            topic='how many times do you drink beer'
        )

        self.client.login(
            username=self.student.username,
            password=self.student.password
        )

        data = {
            'grat_datetime': datetime.datetime(2020, 12, 25, 4, 20),
        }

        response = self.client.post(self.url, data, follow=True)

        self.assertNotEqual(self.session.grat_datetime, data)


    def test_date_and_time_not_can_be_blank(self):
        """
        The date and time of grat test not can be blank.
        """

        pass

    def test_date_and_time_need_to_be_bigger_than_today(self):
        """
        The date and time from grat test need to be bigger than the
        date and time from today and bigger than irat test date/time with its
        duration.
        """

        pass
