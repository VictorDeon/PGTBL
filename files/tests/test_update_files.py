from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from files.models import File

User = get_user_model()


class UpdateFileTestCase(TestCase):
    """
    Test to update a discipline file.
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

        # Create teacher
        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='teacherEmail@email.com',
            password='somepass'
            is_teacher=True
        )

        # Create discipline and discipline file
        self.discipline = mommy.make('Discipline')
        self.discipline.students.add(self.user)
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
        User can not update a file without logged in.
        """
        response = self.client.get(self.url)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url

        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 302)


    def test_update_file_by_teacher(self):
        """
        Test to update a file by teacher.
        """
        self.teacher.login(
            username=self.teacher.username,
            password='somepass'
        )

        url = '/edit/'

        successful_response = self.teacher.get(url, follow=True)

        self.assertEqual(successful_response.status_code, 200)


        pass

    def test_update_file_by_monitors(self):
        """
        Test to update a file by monitors.
        """

        pass

    def test_update_file_fail(self):
        """
        User can not update a file with invalid fields.
        """

        pass

    def test_update_file_by_student_fail(self):
        """
        Student can not update a file.
        """

        pass


class UpdateSessionFileTestCase(TestCase):
    """
    Test to update a session file.
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
        User can not update a file without logged in.
        """

        pass

    def test_update_file_by_teacher(self):
        """
        Test to update a file by teacher.
        """

        pass

    def test_update_file_by_monitors(self):
        """
        Test to update a file by monitors.
        """

        pass

    def test_update_file_fail(self):
        """
        User can not update a file with invalid fields.
        """

        pass

    def test_update_file_by_student_fail(self):
        """
        Student can not update a file.
        """

        pass
