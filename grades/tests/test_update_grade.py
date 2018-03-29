from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from grades.models import Grade, FinalGrade

User = get_user_model()


class UpdateGradeTestCase(TestCase):
    """
    Test to update a specific grade from a specific student.
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
        Teacher can not update a grade without logged in.
        """

        pass

    def test_update_grade_by_teacher(self):
        """
        Test to update a grade by teacher.
        """

        pass

    def test_not_update_grade_by_monitors(self):
        """
        Test to not update a grade by monitors.
        """

        pass

    def test_update_grade_by_student_fail(self):
        """
        Student can not update a grade.
        """

        pass

    def test_update_grade_fail(self):
        """
        Teacher can not update a grade with invalid fields.
        The grande need to be bigger than 0 and smaller than 10.
        """

        pass
