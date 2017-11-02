from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

# Get custom user model
User = get_user_model()


class EditUserTestCase(TestCase):
    """
    Test to edit personal information from user.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.url = reverse('accounts:update-user')
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

    def test_redirect_to_login(self):
        """
        Test to redirect to login page when user try to access the profile
        without be logged.
        """

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        login_url = reverse('accounts:login')
        redirects_url = '{0}?next={1}'.format(login_url, self.url)
        self.assertRedirects(response, redirects_url)

    def test_update_user_ok(self):
        """
        Test to update user personal information with success.
        """

        self.client.login(username=self.user.username, password='test1234')
        data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'institution': 'UnB',
            'course': 'engineering',
        }
        response = self.client.post(self.url, data)
        profile_url = reverse('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.user.refresh_from_db()
        self.assertEquals(self.user.email, 'test@gmail.com')
        self.assertEquals(self.user.username, 'test')

    def test_update_user_email_error(self):
        """
        Test to update with no data.
        """

        self.client.login(username=self.user.username, password='test1234')
        data = {'username': 'test', 'email': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'email', _('This field is required.')
        )

    def test_update_user_username_error(self):
        """
        Test to update with no data.
        """

        self.client.login(username=self.user.username, password='test1234')
        data = {'username': '', 'email': 'test@gmail.com'}
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'username', _('This field is required.')
        )
