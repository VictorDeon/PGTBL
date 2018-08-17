from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse_lazy
from model_mommy import mommy

from core.test_utils import user_factory, check_messages
from disciplines.models import Discipline
from files.models import DisciplineFile

User = get_user_model()


class DisciplineFileTestUpdateCase(TestCase):
    """
    Test to update a discipline file.
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
            slug="discipline01",
            students=[self.student],
            monitors=[self.monitor]
        )

        text_file = SimpleUploadedFile("text.txt", b'This is some text file')
        self.file = mommy.make(
            DisciplineFile,
            title='File title',
            description='File Description',
            extension='txt',
            archive=text_file,
            discipline=self.discipline
        )
        self.url = reverse_lazy(
            'files:update',
            kwargs={
                'slug': self.discipline.slug,
                'pk': self.file.id
            }
        )
        self.client.login(username=self.teacher.username, password='test1234')

    def tearDown(self):
        """
        This method will run after any test.
        """

        User.objects.all().delete()
        self.discipline.delete()
        self.file.delete()

    def test_redirect_to_login(self):
        """
        User can not update a file without logged in.
        """

        self.client.logout()
        response = self.client.get(self.url)
        login_url = reverse_lazy('accounts:login')
        redirect_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirect_url)

    def test_update_file_by_teacher(self):
        """
        Test to update a file by teacher.
        """

        data = {'title': "File title updated", 'extension': 'txt'}
        response = self.client.post(self.url, data, follow=True)
        files_url = reverse_lazy(
            'files:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, files_url)
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, data['title'])
        check_messages(
            self, response,
            tag='alert-success',
            content='File updated successfully.'
        )

    def test_update_file_by_monitors(self):
        """
        Test to update a file by monitors.
        """

        self.client.logout()
        self.client.login(username=self.monitor.username, password='test1234')
        data = {'title': 'File title updated', 'extension': 'txt'}
        response = self.client.post(self.url, data, follow=True)
        files_url = reverse_lazy(
            'files:list',
            kwargs={'slug': self.discipline.slug}
        )
        self.assertRedirects(response, files_url)
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, data['title'])
        check_messages(
            self, response,
            tag='alert-success',
            content='File updated successfully.'
        )

    def test_update_file_fail(self):
        """
        User can not update a file with invalid fields.
        """

        data = {'title': ''}
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(
            response, 'form', 'title', _("This field is required.")
        )
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, 'File title')

    def test_update_file_by_student_fail(self):
        """
        Student can not update a file.
        """

        self.client.logout()
        self.client.login(username=self.student.username, password='test1234')
        data = {'title': 'File title updated'}
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, 'File title')
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )

    def test_update_file_by_user_fail(self):
        """
        Student can not update a file.
        """

        self.client.logout()
        self.client.login(username=self.user.username, password='test1234')
        data = {'title': 'File title updated'}
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse_lazy('accounts:profile'))
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, 'File title')
        check_messages(
            self, response,
            tag='alert-danger',
            content="You are not authorized to do this action."
        )
