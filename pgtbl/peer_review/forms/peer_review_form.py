from django.utils.translation import ugettext_lazy as _
from django import forms
from modules.models import TBLSession


class PeerReviewForm(forms.ModelForm):
    """
    Form to update Peer Review duration and Weight.
    """

    class Meta:
        model = TBLSession
        fields = ['peer_review_available', 'peer_review_weight']


class PeerReviewAnswerForm(forms.Form):
    """
    Form to answer a peer review test.
    """

    score = forms.IntegerField(
        initial=0,
        max_value=100,
        min_value=0,
        label=_("Student score")
    )

    comment = forms.CharField(widget=forms.Textarea, label=_("Student comment"))