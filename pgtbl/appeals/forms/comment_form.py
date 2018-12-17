from django import forms

from appeals.models.comment import Comment


class CommentForm(forms.ModelForm):
    """
    Form to crud a comment.
    """

    class Meta:
        model = Comment
        fields = ['content']