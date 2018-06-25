#Core Django imports
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

#Third-party app imports
from model_mommy import mommy

# Relative imports of the TBL package
from disciplines.models import Discipline

class HallOfFamePageTestCase(TestCase):
    """
    Test to show hallOfFame page.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.discipline1= mommy.make(Discipline)
        pass

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.discipline1.delete()
        
        pass

 
    def test_show_hall_of_fame_to_user(self): 

        client = Client()
        response = client.get(reverse('hallOfFame:list', args=[self.discipline1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hallOfFame/list.html')
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'core/navbar.html')

        pass

