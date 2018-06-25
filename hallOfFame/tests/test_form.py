#Core Django imports
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

# Relative imports of the 'app-name' package
from disciplines.models import Discipline

class HallOfFameFormsTestCase(TestCase):
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

    def test_close_discipline_form_error(self):

        client = Client()
        url = reverse('hallOfFame:list', args=[self.discipline1.slug])
        
        form_data = {'year' : '', 'semester' : ''}
        
        response = client.post(url, form_data)

        #self.assertFormError(response, 'halls', 'year', ) 
        #self.assertFormError(response, 'halls', 'semester', )

        pass

