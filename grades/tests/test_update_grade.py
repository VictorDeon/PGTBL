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
        self.client = Client()
        self.discipline = mommy.make('Discipline')
        self.session = mommy.make('TBLSession')        
        self.teacher = User.objects.create_user(
            username='teacher',
            email='tea@gmail.com',
            password='senha123',
            is_teacher=True,
        )
        self.student = User.objects.create_user(
            username='student',
            email='stu@gmail.com',
            password='senha123',
        )
        self.url = reverse_lazy('grades:update', kwargs={
            'slug': self.discipline.slug, 
            'pk': self.session.pk,
            'student_pk': self.student.pk
        })
        self.login_redirect = '/login/?next=' + str(self.url)

    def tearDown(self):
        """
        This method will run after any test.
        """

        pass

    def test_redirect_to_login(self):
        """
        Teacher can not update a grade without logged in.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_redirect, status_code=302, target_status_code=200)

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
