import pytest
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from core.test_utils import check_messages
from django.core.urlresolvers import reverse
from model_mommy import mommy
from files.models import DisciplineFile, File, SessionFile
from accounts.models import User
from TBLSessions.models import TBLSession

User = get_user_model()


class DeleteFileTestCase(TestCase):
    """
    Test to delete a discipline file.
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
        self.teacher = User.objects.create_user(
            username='testteacher',
            email='testteacher@anymail.com',
            password='testteacher123',
            is_teacher=True
        )
        self.monitor = User.objects.create_user(
            username='someMonitor',
            email='monitorEmail@email.com',
            password='someMonitorpass',
            is_teacher=True
        )

        self.discipline = mommy.make('Discipline')
        self.discipline.teacher = self.teacher
        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )
        self.tbl_session = self.tbl_sessions[0]

        self.file = mommy.make('DisciplineFile')

        self.file.discipline = self.discipline


    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not delete a file without logged in.
        """
        url_login = reverse('accounts:login')
        url_file_delete = reverse('files:delete', kwargs={'slug': self.tbl_session.discipline.slug, 'pk': self.file.pk})
        redirect_url = url_login + '?next=' + url_file_delete
        response = self.client.get(url_file_delete.rstrip('/'), follow=True)
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 301)

    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """
        self.client.login(username=self.teacher.username, password='testteacher123')
        file_before = File.objects.all().count()
        request = self.file
        url_file_delete = reverse('files:delete', kwargs={'slug': self.tbl_session.discipline.slug, 'pk': self.file.pk})
        response = self.client.delete(url_file_delete)
        res = self.client.get(url_file_delete)
        print(url_file_delete)
        print(response)
        file_after = File.objects.all().count()
        print(file_before)
        print(file_after)
        teste = file_before > file_after
        self.assertTrue(teste)


    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """

        pass

    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """

        pass

class DeleteSessionFileTestCase(TestCase):
    """
    Test to delete a session file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        pass

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not delete a file without logged in.
        """

        pass

    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """

        pass

    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """

        pass

    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """

        pass
