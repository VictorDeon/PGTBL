from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from modules.models import TBLSession

User = get_user_model()


class DetailPracticalTestCase(TestCase):
    """
    Test to show the practical test.
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

    def test_show_practical_test_to_student(self):
        """
        The practical test need to be opened by teacher for student to see
        """

        pass

    def test_teacher_and_monitor_can_see_practical_test(self):
        """
        Teacher and monitors that is a teacher can see the practical test,
        before it being opened.
        """

        pass
