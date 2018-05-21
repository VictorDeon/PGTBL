from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from files.models import File

User = get_user_model()


class CreateFileTestCase(TestCase):
    """
    Test to create a new discipline file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()

        # Create user
        self.user = User.objects.create_user(
            username='Testuser',
            email='user@email.com',
            password='tester123')

        #Create teacher
        self.teacher = User.objects.create_user(
            username='Testteacher',
            email='teacher@email.com',
            password='tester123',
            is_teacher=True
        )

        #Create monitor
        self.monitor = User.objects.create_user(
            username='Testmonitor',
            email='monitor@email.com',
            password='tester123',
            is_teacher=True
        )

        #Create discipline
        self.discipline = mommy.make('Discipline')
        self.discipline.teacher = self.teacher
        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=15
        )
        self.tbl_session = self.tbl_sessions[0]

        #Create file url
        self.url_file_create = reverse('files:create')

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.client.logout()
        self.user.delete()

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """
        response = self.client.get(self.url_file_create)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url_file_create

        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, redirect_url, 302)
        

    def test_create_file_by_teacher(self):
        """
        Test to create a new file by teacher.
        """
        self.client.login(username=self.teacher.username, password='tester123')
        file_before = File.objects.all().count()
        response = self.client.create(self.url_file_create)
        res = self.client.get(url_file_create)
        file_after = File.objects.all().count()

        test = file_before < file_after
        self.assertTrue(test)

    def test_create_file_by_monitors(self):
        """
        Test to create a new file by monitors.
        """
        self.client.login(username=self.monitor.username, password='tester123')
        file_before = File.objects.all().count()
        response = self.client.create(self.url_file_create)
        res = self.client.get(url_file_create)
        file_after = File.objects.all().count()

        test = file_before < file_after
        self.assertTrue(test)

    def test_create_file_fail(self):
        """
        User can not create a file with invalid fields.
        """
        self.client.login(username=self.teacher.username, password='tester123')
        file_before = File.objects.all().count()
        response = self.client.create(self.url_file_create)
        res = self.client.get(url_file_create)
        file_after = File.objects.all().count()

        test = file_before == file_after
        self.assertTrue(test)

    def test_create_file_by_student_fail(self):
        """
        Student can not create a file.
        """
        self.client.login(username=self.user.username, password='tester123')
        file_before = File.objects.all().count()
        response = self.client.create(self.url_file_create)
        res = self.client.get(url_file_create)
        file_after = File.objects.all().count()

        test = file_before == file_after
        self.assertTrue(test)


class CreateSessionFileTestCase(TestCase):
    """
    Test to create a new session file.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()

        # Create user
        self.user = User.objects.create_user(
            username='Testuser',
            email='user@email.com',
            password='tester123')

        #Create teacher
        self.teacher = User.objects.create_user(
            username='Testteacher',
            email='teacher@email.com',
            password='tester123',
            is_teacher=True
        )

        #Create monitor
        self.monitor = User.objects.create_user(
            username='Testmonitor',
            email='monitor@email.com',
            password='tester123',
            is_teacher=True
        )

        #Create discipline
        self.discipline = mommy.make('Discipline')
        self.discipline.teacher = self.teacher
        self.tbl_sessions = mommy.make(
            TBLSession,
            discipline=self.discipline,
            _quantity=15
        )
        self.tbl_session = self.tbl_sessions[0]

        #Create file url
        self.url_file_create = reverse('files:session-create')

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        User can not create a new file without logged in.
        """
        response = self.client.get(self.url_file_create)
        url_login = reverse('accounts:login')
        redirect_url = url_login + '?next=' + self.url_file_create

        self.assertTrue(response.status_code, 301)
        self.assertRedirects(response, redirect_url, 302)

    def test_create_file_by_teacher(self):
        """
        Test to create a new file by teacher.
        """

        pass

    def test_create_file_by_monitors(self):
        """
        Test to create a new file by monitors.
        """

        pass

    def test_create_file_fail(self):
        """
        User can not create a file with invalid fields.
        """

        pass

    def test_create_file_by_student_fail(self):
        """
        Student can not create a file.
        """

        pass
