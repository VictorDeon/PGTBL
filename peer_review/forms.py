from django import forms

from TBLSessions.models import TBLSession
from .models import PeerReview


class PeerReviewUpdateForm(forms.ModelForm):
    """
    Form to update Peer Review duration and weight.
    """

    class Meta:
        model = TBLSession
        fields = [
            'peer_review_weight',
            'peer_review_duration',
        ]


class PeerReviewDateForm(forms.ModelForm):
    """
    Form to update datetime of Peer Review.
    """

    peer_review_datetime = forms.DateTimeField(
        label="Date and time to provide the peer review",
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'] # '2016-04-06T17:18
    )

    class Meta:
        model = TBLSession
        fields = ['peer_review_datetime']


class StudentForm(forms.ModelForm):
    """
    Form for student to make Peer Review.
    """
    class Meta:
        model = PeerReview
        fields = ['feedback',
                  'score']
