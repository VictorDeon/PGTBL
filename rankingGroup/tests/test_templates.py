#Core Django imports
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

# Relative imports of the 'app-name' package
from disciplines.models import Discipline

class RankingGroupPageTestCase(TestCase):
    """
    Test to show rankingGroup page.
    """

    def setUp(self):
        self.discipline1= mommy.make(Discipline)
        pass

    def tearDown(self):
        self.discipline1.delete()
        
        pass

 
    def test_show_ranking_group_to_user(self): 

        client = Client()
        response = client.get(reverse('ranking:list', args=[self.discipline1.slug]))
        self.assertEqual(response.status_code, 200)
        

        pass

