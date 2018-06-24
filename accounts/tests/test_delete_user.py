from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from core.test_utils import check_messages

# Get custom user model
User = get_user_model()


class DeleteUserTestCase(TestCase):
    """
    Test to delete a user account.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.url = reverse('accounts:delete-user')
        self.user = User.objects.create_user(
            username='teste',
            email='teste@gmail.com',
            password='test1234'
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

    def test_delete_user_ok(self):
        """
        Test to delete user with success.
        """

        self.assertEquals(User.objects.count(), 1)
        self.client.login(username=self.user.username, password='test1234')
        response = self.client.post(self.url, follow=True)
        home_url = reverse('core:home')
        self.assertRedirects(response, home_url)
        self.assertEquals(User.objects.count(), 0)
        check_messages(
            self, response,
            tag='alert-success',
            content="Accounts deleted successfully."
        )
