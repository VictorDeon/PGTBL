from django import forms
from .models import PeerReview, PeerReviewFormModel


class Student1Form(forms.ModelForm):

    class Meta:
        model = PeerReviewFormModel
        fields = ['feedback',
                  'score']


class Student2Form(forms.ModelForm):

    class Meta:
        model = PeerReviewFormModel
        fields = ['feedback',
                  'score']


class Student3Form(forms.ModelForm):

    class Meta:
        model = PeerReviewFormModel
        fields = ['feedback',
                  'score']


class Student4Form(forms.ModelForm):

    class Meta:
        model = PeerReviewFormModel
        fields = ['feedback',
                  'score']


class Student5Form(forms.ModelForm):

    class Meta:
        model = PeerReviewFormModel
        fields = ['feedback',
                  'score']
