#Core Django imports
from django.test import TestCase
import datetime

# Relative imports of the TBL package
from hallOfFame.form import HallOfFameForm

class HallOfFameFormsTestCase(TestCase):
    """
    Test to show hallOfFame page.
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

    def test_close_discipline_form_submitted_successfully(self):
        '''
        Tests if the close discipline form was submitted with appropriate data.
        '''

        current_year = datetime.date.today().year
        form_data = {'year' : current_year, 'semester' : '1'}

        form = HallOfFameForm(data=form_data)
        
        self.assertTrue(form.is_valid())
