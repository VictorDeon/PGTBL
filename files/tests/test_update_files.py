from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from disciplines.models import File

User = get_user_model()


class UpdateFileTestCase(TestCase):
    """
    Test to update a discipline file.
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
