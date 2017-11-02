from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from core.test_utils import check_messages
from rolepermissions.checkers import has_role

# Get custom user model
User = get_user_model()


class RegisterTestCase(TestCase):
    """
    Test to register a new user into the system.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.register_url = reverse('accounts:register')
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

    def test_register_teacher_ok(self):
        """
        Test that verify if the new teacher is successfully registered.
        """

        data = {
            'username': 'person1',
            'email': 'person1@gmail.com',
            'is_teacher': True,
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.assertEquals(User.objects.count(), 1)
        response = self.client.post(self.register_url, data, follow=True)
        self.assertEquals(User.objects.count(), 2)
        profile_url = reverse('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertTrue(
            has_role(
                User.objects.get(username='person1'),
                ['teacher']
            )
        )
        check_messages(
            self, response,
            tag='alert-success',
            content='Teacher created successfully.'
        )

    def test_register_student_ok(self):
        """
        Test that verify if the new student is successfully registered.
        """

        data = {
            'username': 'person2',
            'email': 'person2@gmail.com',
            'is_teacher': False,
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.assertEquals(User.objects.count(), 1)
        response = self.client.post(self.register_url, data, follow=True)
        self.assertEquals(User.objects.count(), 2)
        profile_url = reverse('accounts:profile')
        self.assertRedirects(response, profile_url)
        self.assertTrue(
            has_role(
                User.objects.get(username='person2'),
                ['student']
            )
        )
        check_messages(
            self, response,
            tag='alert-success',
            content='Student created successfully.'
        )

    def test_username_register_error(self):
        """
        Test that get the empty username when the user try to register.
        """

        data = {
            'email': 'person@gmail.com',
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.register_error(
            data,
            'username',
            'This field is required.'
        )

    def test_email_register_error(self):
        """
        Test that get the empty email when the user try to register.
        """

        data = {
            'username': 'person',
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.register_error(
            data,
            'email',
            'This field is required.'
        )

    def test_invalid_password(self):
        """
        Test that verify incorrect password match.
        """

        data = {
            'username': 'person',
            'email': 'person@gmail.com',
            'password1': 'test1234',
            'password2': 'test12345'
        }
        self.register_error(
            data,
            'password2',
            "The two password fields didn't match."
        )

    def test_try_to_register_same_username(self):
        """
        Try to register a user with a username that already exists.
        """

        data = {
            'username': 'teste',
            'email': 'person@gmail.com',
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.register_error(
            data,
            'username',
            "A user with that username already exists."
        )

    def test_try_to_register_same_email(self):
        """
        Try to register a user with a email that already exists.
        """

        data = {
            'username': 'person',
            'email': 'teste@gmail.com',
            'password1': 'test1234',
            'password2': 'test1234'
        }
        self.register_error(
            data,
            'email',
            "A user with that email already exists."
        )

    def register_error(self, data, field, error):
        self.assertEquals(User.objects.count(), 1)
        response = self.client.post(self.register_url, data)
        self.assertFormError(
            response,
            'form',
            field,
            _(error)
        )
        self.assertEquals(User.objects.count(), 1)
