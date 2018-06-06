from django import forms

from TBLSessions.models import TBLSession
from .models import PeerReview


class PeerReviewUpdateForm(forms.ModelForm):
    """
    Form to update Peer Review duration and weight.
    """

    class Meta:
        model = TBLSession
        fields = ['peer_review_available', 'peer_review_weight']


class StudentForm(forms.ModelForm):
    """
    Form for student to make Peer Review.
    """
    class Meta:
        model = PeerReview
        fields = ['feedback',
                  'score']
