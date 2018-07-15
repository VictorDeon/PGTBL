from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core import mail
from accounts.models import PasswordReset
from core.test_utils import check_messages

User = get_user_model()


class ResetPasswordTestCase(TestCase):
    """
    Test to reset accounts password.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """

        self.client = Client()
        self.user = User.objects.create_user(
            username='Test1',
            email='test1@gmail.com',
            password='test1234',
            is_teacher=True
        )
        self.url = reverse_lazy('accounts:reset-password')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.user.delete()

    def test_send_email_to_reset_password(self):
        """
        Test to send email to reset password.
        """

        data = {'email': 'test1@gmail.com'}
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, _("Requesting new password"))

    def test_send_email_fail(self):
        """
        Test send email with invalid inputs.
        """

        data = {'email': ''}

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'email', _('This field is required.')
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_send_email_to_nonexistent_email(self):
        """
        Test send email to an email nonexistent
        """

        data = {'email': 'nonexistent@gmail.com'}

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'email',
            _('There is no user found with this email')
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_ok(self):
        """
        Teste to reset password after receive the link in email.
        """

        reset_password = PasswordReset.objects.create(
            user=self.user,
            key='12345'
        )
        url = reverse_lazy(
            'accounts:reset-password-confirm',
            kwargs={'key': reset_password.key}
        )
        data = {
            'old_password': 'test1234',
            'new_password1': 'test12345678',
            'new_password2': 'test12345678'
        }
        response = self.client.post(url, data, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('test12345678'))
        check_messages(
            self, response,
            tag='alert-success',
            content="Your password was successfully updated."
        )
