from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from django.conf import settings

# Get custom user model
User = get_user_model()


class LoginTestCase(TestCase):
    """
    Test all features about login.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            username='teste',
            email='teste@gmail.com',
            password='test1234',
            is_teacher=True
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.user.delete()

    def test_username_login_ok(self):
        """
        Test that verify if the username login is working successfully
        """

        self.login_successful(self.user.username, 'test1234')

    def test_email_login_ok(self):
        """
        Test that verify if the username login is working successfully
        """

        self.login_successful(self.user.email, 'test1234')

    def test_login_password_error(self):
        """
        Test that verify a password incorrect error.
        """

        self.login_error(self.user.username, 'password incorrect')

    def test_login_username_error(self):
        """
        Test that verify a password incorrect error.
        """

        self.login_error('incorrect username', 'test1234')

    def login_successful(self, username, password):
        """
        Function that veirfy the correct username or email and password
        """

        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTrue(not response.wsgi_request.user.is_authenticated)
        data = {'username': username, 'password': password}
        response = self.client.post(self.login_url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def login_error(self, username, password):
        """
        Function that verify a specific field incorrect error.
        """

        data = {'username': username, 'password': password}
        response = self.client.post(self.login_url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        error_msg = (_(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ))
        self.assertFormError(
            response,
            'form',
            None,
            error_msg % {'username': _('User')}
        )
