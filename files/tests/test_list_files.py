from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.test import Client, TestCase
from django.urls import reverse
from model_mommy import mommy

from accounts.models import User
from core.test_utils import check_messages
from disciplines.models import Discipline
from files.models import DisciplineFile, File, SessionFile
from TBLSessions.models import TBLSession

User = get_user_model()


class ListFileTestCase(TestCase):
    """
    Test to list discipline files.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        # Create user
        self.user = User.objects.create_user(
            username='tester',
            email='tester@tester.com',
            password='tester123')

        self.discipline = mommy.make('Discipline')
        self.discipline.students.add(self.user)

        # Create file at discipline
        for i in range(1, 15):
            self.discipline_file = DisciplineFile.objects.create(
                extension='.jpg',
                title='test',
                archive='test.jpg',
                discipline=self.discipline)

        # Setup client and base url
        self.client = Client()
        self.url = reverse('files:list', args=[self.discipline.slug])

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.client.logout()
        self.user.delete()

    def test_redirect_to_login(self):
        """
        User can not see the file list without logged in.
        """
        response = self.client.get(self.url)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url

        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 302)

    def test_file_pagination(self):
        """
        Test to show files by pagination.
        """
        self.client.login(username='tester', password='tester123')

        response = self.client.get(self.url)
        pages = response.context_data['paginator']
        page1 = pages.page(1)
        page2 = pages.page(2)

        # Expect to have two pages
        self.assertTrue(page1.number, 1)
        self.assertTrue(page2.number, 2)

    def test_users_can_see_the_files(self):
        """
        User like students, monitors and teacher can see the list of files.
        """

        self.client.login(username='tester', password='tester123')
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)


class ListSessionFileTestCase(TestCase):
    """
    Test to list session files.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        # Create user
        self.user = User.objects.create_user(
            username='tester',
            email='tester@tester.com',
            password='tester123')

        self.discipline = mommy.make('Discipline')
        self.discipline.students.add(self.user)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=5
        )
        self.tbl_session = self.tbl_sessions[0]

        # Create file at discipline
        for i in range(1, 15):
            self.session_file = SessionFile.objects.create(
                extension='.jpg',
                title='test',
                archive='test.jpg',
                session=self.tbl_session)

        # Setup client and base url
        self.client = Client()
        self.url = reverse('files:session-list',
                           args=[self.discipline.slug, 1])

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.client.logout()
        self.user.delete()

    def test_redirect_to_login(self):
        """
        User can not see the file list without logged in.
        """
        response = self.client.get(self.url)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url

        self.assertTrue(response.status_code, 301)
        self.assertRedirects(response, redirect_url, 302)

    def test_file_pagination(self):
        """
        Test to show files by pagination. If session is opened.
        """
        self.client.login(username='tester', password='tester123')

        response = self.client.get(self.url)
        pages = response.context_data['paginator']
        page1 = pages.page(1)
        page2 = pages.page(2)

        # Expect to have two pages
        self.assertTrue(page1.number, 1)
        self.assertTrue(page2.number, 2)

    def test_users_can_see_the_files(self):
        """
        User like students, monitors and teacher can see the list of files.
        if the session is opened.
        """

        self.client.login(username='tester', password='tester123')
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)
