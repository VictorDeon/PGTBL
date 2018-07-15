from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from files.models import ModuleFile

User = get_user_model()


class ModuleFileCreateTestCase(TestCase):
    """
    Test to create a new module file.
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
        User can not create a new file without logged in.
        """

        pass

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
