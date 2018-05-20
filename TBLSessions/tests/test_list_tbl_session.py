from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession

User = get_user_model()


class ListTBLSessionTestCase(TestCase):
    """
    Test to list tbl sessions.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()

        self.student = User.objects.create_user(
            username='testusername',
            email='testusername@anymail.com',
            password='pwdtestuser123'
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.students.add(self.student)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )
        self.tbl_session = self.tbl_sessions[0]


        


    def tearDown(self):
        """
        This method will run after any test.
        """
        self.student.delete()
        for tbl in self.tbl_sessions:
            tbl.delete()

        

    def test_redirect_to_login(self):
        """
        User can not see the tbl session list without logged in.
        """
        url = '/profile/{}/sessions'.format(
            self.tbl_session.discipline.slug
        )

        failed_response = self.client.get(url, follow=True)

        redirect_to = '/login/?next=/profile/{}/sessions/'.format(
            self.tbl_session.discipline.slug
        )

        self.assertRedirects(failed_response, redirect_to, 301)
        

    def test_tbl_session_pagination(self):
        """
        Test to show tbl session by pagination.
        """

        self.client.login(
            username=self.student.username,
            password='pwdtestuser123'
        )

        # Expects all pages from 1 to 6 to respond with 200
        for page_index in range(1, 7):
            page_url = '/profile/{}/sessions/?page={}'.format(
                self.tbl_session.discipline.slug,
                page_index
            )

            response = self.client.get(page_url, follow=True)

            self.assertEqual(response.status_code, 200)

    def test_users_can_see_the_tbl_sessions(self):
        """
        User like students, monitors and teacher can see the list of tbl
        sessions.
        """
        url = '/profile/{}/sessions'.format(
            self.tbl_session.discipline.slug
        )

        self.client.login(
            username=self.student.username,
            password='pwdtestuser123'
        )

        successful_response = self.client.get(url, follow=True)

        self.assertEqual(successful_response.status_code, 200)


