#Core Django imports
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

#Third-party app imports
from model_mommy import mommy

# Relative imports of the TBL package
from disciplines.models import Discipline
from accounts.models import User

class RankingGroupPageTestCase(TestCase):
    """
    Test to show rankingGroup page.
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

    def test_if_teacher_can_access_ranking(self):
        """
        Tests if the teacher who created the discipline can access it.
        """

        #Objects and client
        client = Client()
        self.teacher1= mommy.make(User, name='teacher1', password='12345', is_teacher=True)
        self.discipline_teacher= mommy.make(Discipline, teacher=self.teacher1)

        response = self.client.get(reverse('ranking:list', args=[self.discipline_teacher.slug]))

        user = authenticate(client, username='teacher1', password='12345')

        if user is not None:
            #Check that we got a response "success"
            self.assertEqual(response.status_code, 200) 
            self.assertTemplateUsed(response, 'rankingGroup/detail.html')
        else:
            # Invalid login - redirect to the login page.
            self.assertEqual(response.status_code, 302) 

        self.teacher1.delete()
        self.discipline_teacher.delete()

        pass

    def test_if_students_can_access_ranking(self):
        """
        Tests whether the students who belong to the discipline can access it.
        """

        #Objects and client
        client = Client()
        self.student1= mommy.make(User, name='student1', password='12345', is_teacher=False)
        self.student2= mommy.make(User, name='student3', password='12345', is_teacher=False)
        self.student3= mommy.make(User, name='student2', password='12345', is_teacher=False)
        self.discipline_students= mommy.make(Discipline, students=[self.student1, self.student2, self.student3])

        response = self.client.get(reverse('ranking:list', args=[self.discipline_students.slug]))

        user1 = authenticate(client, username='student1', password='12345')
        user2 = authenticate(client, username='student2', password='12345')
        user3 = authenticate(client, username='student3', password='12345')

        if user1 and user2 and user3 is not None:
            #Check that we got a response "success".
            self.assertEqual(response.status_code, 200) 
            self.assertTemplateUsed(response, 'rankingGroup/detail.html')
        else:
            # Invalid login - redirect to the login page.
            self.assertEqual(response.status_code, 302) 

        self.student1.delete()
        self.student2.delete()
        self.student3.delete()
        self.discipline_students.delete()

        pass

    def test_if_monitors_can_access_ranking(self):
        """
        Tests whether the monitors who belong to the discipline can access it.
        """

        #Objects and client
        client = Client()
        self.monitor1= mommy.make(User, name='monitor1', password='12345', is_teacher=False)
        self.monitor2= mommy.make(User, name='monitor3', password='12345', is_teacher=False)
        self.discipline_monitors= mommy.make(Discipline, monitors=[self.monitor1, self.monitor2])

        response = self.client.get(reverse('ranking:list', args=[self.discipline_monitors.slug]))

        user1 = authenticate(client, username='monitor1', password='12345')
        user2 = authenticate(client, username='monitor2', password='12345')

        if user1 and user2 is not None:
            #Check that we got a response "success".
            self.assertEqual(response.status_code, 200) 
            self.assertTemplateUsed(response, 'rankingGroup/detail.html')
        else:
            # Invalid login - redirect to the login page.
            self.assertEqual(response.status_code, 302) 

        self.monitor1.delete()
        self.monitor2.delete()
        self.discipline_monitors.delete()

        pass