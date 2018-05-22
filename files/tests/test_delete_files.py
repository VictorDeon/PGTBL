import pytest
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from core.test_utils import check_messages
from django.core.urlresolvers import reverse
from model_mommy import mommy
from files.models import DisciplineFile, File, SessionFile
from accounts.models import User
from disciplines.models import Discipline
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

        self.teacher = User.objects.create_user(
            username='professorTeste',
            email='professorteste@email.com',
            password='professorTeste123',
            is_teacher=True
        )

        self.monitor = User.objects.create_user(
            username='monitorTeste',
            email='monitorteste@email.com',
            password='monitorTeste123',
            is_teacher=True
        )

        self.student = User.objects.create_user(
            username='estudanteTeste',
            email='estudanteteste@anymail.com',
            password='estudanteTeste123'
        )

        self.discipline = Discipline.objects.create(
            title='Discipline01',
            description='Discipline description.',
            classroom='Class A',
            students_limit=59,
            monitors_limit=5,
            is_closed=True,
            teacher=self.teacher,
            slug='discipline01'
        )
        self.discipline.monitors.add(self.monitor)
        self.discipline.students.add(self.student)
        #self.discipline.save()

        self.discipline_file = DisciplineFile.objects.create(
            extension='.jpg',
            title='test',
            archive='test.jpg',
            discipline=self.discipline)
        self.discipline_file.save()

        self.url = reverse(
            'files:delete',
            args=[self.discipline.slug, self.discipline_file.pk]
        )

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=30
        )


    def tearDown(self):
        """
        This method will run after any test.
        """
        self.client.logout()
        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()
        self.discipline.delete()

    def test_redirect_to_login(self):
        """
        User can not delete a file without logged in.
        """
        url_login = reverse('accounts:login')
        url_file_delete = self.url
        redirect_url = url_login + '?next=' + url_file_delete
        response = self.client.get(url_file_delete.rstrip('/'), follow=True)
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 301)

    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """
        self.client.login(username=self.teacher.username, password='professorTeste123')
        file_before = File.objects.all().count()
        response = self.client.delete(self.url)
        file_after = File.objects.all().count()
        teste = file_before > file_after
        self.assertTrue(teste)

    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """
        self.client.login(username=self.monitor.username, password='monitorTeste123')
        file_before = File.objects.all().count()
        response = self.client.delete(self.url)
        file_after = File.objects.all().count()
        teste = file_before > file_after
        self.assertTrue(teste)


    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """
        self.client.login(username=self.student.username, password='estudanteTeste123')
        file_before = File.objects.all().count()
        response = self.client.delete(self.url)
        file_after = File.objects.all().count()
        teste = file_before > file_after
        self.assertFalse(teste)



class DeleteSessionFileTestCase(TestCase):
    """
    Test to delete a session file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()

        self.teacher = User.objects.create_user(
            username='professorTeste',
            email='professorteste@email.com',
            password='professorTeste123',
            is_teacher=True
        )

        self.monitor = User.objects.create_user(
            username='monitorTeste',
            email='monitorteste@email.com',
            password='monitorTeste123',
            is_teacher=True
        )

        self.student = User.objects.create_user(
            username='estudanteTeste',
            email='estudanteteste@anymail.com',
            password='estudanteTeste123'
        )

        self.discipline = Discipline.objects.create(
            title='Discipline01',
            description='Discipline description.',
            classroom='Class A',
            students_limit=59,
            monitors_limit=5,
            is_closed=True,
            teacher=self.teacher,
            slug='discipline01'
        )
        self.discipline.monitors.add(self.monitor)
        self.discipline.students.add(self.student)

        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=5
        )
        self.tbl_session = self.tbl_sessions[0]

        self.session_file = SessionFile.objects.create(
            extension='.jpg',
            title='test',
            archive='test.jpg',
            session=self.tbl_session)

        self.url = reverse(
                    'files:session-delete',
                    args=[self.discipline.slug, self.tbl_session.pk, self.session_file.file_ptr_id]
        )


    def tearDown(self):
        """
        This method will run after any test.
        """
        self.client.logout()
        self.teacher.delete()
        self.monitor.delete()
        self.student.delete()
        self.discipline.delete()


    def test_redirect_to_login(self):
        """
        User can not delete a file without logged in.
        """
        response = self.client.get(self.url)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url

        self.assertTrue(response.status_code, 301)
        self.assertRedirects(response, redirect_url, 302)


    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """
        self.client.login(username=self.teacher.username, password='professorTeste123')
        file_before = SessionFile.objects.all().count()
        response = self.client.delete(self.url)
        file_after = SessionFile.objects.all().count()
        teste = file_before > file_after
        self.assertTrue(teste)

    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """
        self.client.login(username=self.monitor.username, password='monitorTeste123')
        file_before = SessionFile.objects.all().count()
        response = self.client.delete(self.url)
        file_after = SessionFile.objects.all().count()
        teste = file_before > file_after
        self.assertTrue(teste)

    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """
        self.client.login(username=self.student.username, password='estudanteTeste123')
        file_before = SessionFile.objects.all().count()
        response = self.client.delete(self.url)
        file_after = SessionFile.objects.all().count()
        teste = file_before > file_after
        self.assertFalse(teste)
