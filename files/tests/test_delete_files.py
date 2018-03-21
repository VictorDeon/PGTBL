from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import File

User = get_user_model()


class DeleteFileTestCase(TestCase):
    """
    Test to delete a discipline file.
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
        User can not delete a file without logged in.
        """

        pass

    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """

        pass

    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """

        pass

    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """

        pass

class DeleteSessionFileTestCase(TestCase):
    """
    Test to delete a session file.
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
        User can not delete a file without logged in.
        """

        pass

    def test_delete_file_by_teacher(self):
        """
        Test to delete a file by teacher.
        """

        pass

    def test_delete_file_by_monitors(self):
        """
        Test to delete a file by monitors.
        """

        pass

    def test_delete_file_by_student_fail(self):
        """
        Student can not delete a file.
        """

        pass
