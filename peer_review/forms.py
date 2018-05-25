from django import forms
from django.contrib.auth import get_user_model
from .models import PeerReview

# Get the user from settings
User = get_user_model()

class PeerReviewForm(forms.ModelForm):

    class Meta:
        model = PeerReview
        fields = ['username_received',
                  'username_gave',
                  'feedback',
                  'score']
