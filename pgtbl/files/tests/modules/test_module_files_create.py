from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import user_factory, check_messages, create_image
from model_mommy import mommy

from disciplines.models import Discipline
from files.models import ModuleFile
from modules.models import TBLSession

User = get_user_model()


class SessionFileCreateTestCase(TestCase):
    """
    Test to create a new session file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.teacher = user_factory(name="maria", is_teacher=True)
        self.monitor = user_factory(name="pedro", is_teacher=False)
        self.student = user_factory(name="joao", is_teacher=False)
        self.user = user_factory(name="miguel", is_teacher=True)
        self.discipline = mommy.make(
            Discipline,
            teacher=self.teacher,
            title="Discipline",
            course="Course",
            classroom="Class A",
            password="12345",
            students=[self.student],
            monitors=[self.monitor]
        )
        self.module = mommy.make(
            TBLSession,
            discipline=self.discipline,
            title="Module test",
            description="Description test"
        )
        self.url = reverse_lazy(
            'files:module-create',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.module.pk
            }
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.module.delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """

        self.client.logout()
        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_create_file_image_by_teacher(self):
        """
        Test to create a new image by teacher.
        """

        avatar = create_image(None, 'avatar.png')
        avater_file = SimpleUploadedFile("avatar.png", avatar.getvalue())

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'PNG',
            'archive': avater_file,
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 1)
        check_messages(
            self, response,
            tag="alert-success",
            content="File created successfully."
        )

    def test_create_file_by_teacher(self):
        """
        Test to create a new file by teacher.
        """

        text_file = SimpleUploadedFile("text.txt", b'This is some text file')

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'TXT',
            'archive': text_file,
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.teacher.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 1)
        check_messages(
            self, response,
            tag="alert-success",
            content="File created successfully."
        )

    def test_create_file_by_monitors(self):
        """
        Test to create a new file by monitors.
        """

        text_file = SimpleUploadedFile("text.txt", b'This is some text file')

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'TXT',
            'archive': text_file,
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 1)
        check_messages(
            self, response,
            tag="alert-success",
            content="File created successfully."
        )

    def test_create_file_fail(self):
        """
        User can not create a file without a file.
        """

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'TXT',
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.monitor.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 0)
        check_messages(
            self, response,
            tag="alert-danger",
            content="Invalid fields, please fill in the fields correctly."
        )

    def test_create_file_by_student_fail(self):
        """
        Student can not create a file.
        """

        text_file = SimpleUploadedFile("text.txt", b'This is some text file')

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'TXT',
            'archive': text_file,
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.student.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 0)
        check_messages(
            self, response,
            tag="alert-danger",
            content="You are not authorized to do this action."
        )

    def test_create_file_by_user_fail(self):
        """
        User that is not in the discipline can not create a file.
        """

        text_file = SimpleUploadedFile("text.txt", b'This is some text file')

        data = {
            'title': 'File title',
            'description': 'File Description',
            'extension': 'TXT',
            'archive': text_file,
            'session': self.module
        }

        self.assertEqual(ModuleFile.objects.count(), 0)
        self.client.login(username=self.user.username, password='test1234')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(ModuleFile.objects.count(), 0)
        check_messages(
            self, response,
            tag="alert-danger",
            content="You are not authorized to do this action."
        )