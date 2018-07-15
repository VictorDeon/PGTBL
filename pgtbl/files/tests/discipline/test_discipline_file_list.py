from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from files.models import DisciplineFile

User = get_user_model()


class DisciplineFileListTestCase(TestCase):
    """
    Test to list discipline files.
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
        User can not see the file list without logged in.
        """

        pass

    def test_file_pagination(self):
        """
        Test to show files by pagination.
        """

        pass

    def test_users_can_see_the_files(self):
        """
        User like students, monitors and teacher can see the list of files.
        """

        pass
