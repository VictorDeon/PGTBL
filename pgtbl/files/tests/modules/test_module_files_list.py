from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from files.models import ModuleFile

User = get_user_model()


class ModuleFileListTestCase(TestCase):
    """
    Test to list module files.
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
        Test to show files by pagination. If session is opened.
        """

        pass

    def test_users_can_see_the_files(self):
        """
        User like students, monitors and teacher can see the list of files.
        if the session is opened.
        """

        pass
