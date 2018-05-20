from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from questions.models import (
    Question, Alternative, ExerciseSubmission,
    IRATSubmission, GRATSubmission
)

User = get_user_model()


class GRATResultTestCase(TestCase):
    """
    Test to show grat test result.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        # Preparing TBL Section
        self.client = Client()
        self.student = User.objects.create_user(
            username='estudante',
            email='estudante@email.com',
            password='estudate123'
        )
        self.tbl_session = mommy.make('TBLSession')
        self.tbl_session.discipline.students.add(self.student)



    def tearDown(self):
        """
        This method will run after any test.
        """
        self.student.delete()
        self.tbl_session.delete()





    def test_user_can_see_grat_result(self):
        """
        User like student, teacher and monitors can see the result of grat
        after the test is over or if student finish the test.
        """
        # /profile/materia/sessions/pk/grat/result
        url = '/profile/{}/sessions/{}/grat/result'.format(
            self.tbl_session.discipline.slug,
            self.tbl_session.pk
        )
        
        self.client.login(
            username=self.student.username,
            password='estudante123'
        )

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)



    def test_show_only_not_exercise_question(self):
        """
        Show only not exercise question that are into grat test, and show the
        answers.
        """
        pass




        
        



    def test_calcule_the_grat_result(self):
        """
        Calcule the grat test result from grat test.
        score that the group made, total of scores and grade of group.
        Only students have grade created.
        """
        pass
        
        

    def test_group_submit_test_only_once(self):
        """
        The student group can submit the test only once. Only one
        member of group need to submit the test.
        """

        pass

    def test_student_need_to_be_into_a_group(self):
        """
        User without group can not submit the test.
        """

        pass
