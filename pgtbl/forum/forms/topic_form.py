from django import forms
from pagedown.widgets import PagedownWidget

from forum.models import Topic


class TopicForm(forms.ModelForm):
    """
    Form to crud a topic.
    """

    class Meta:
        model = Topic
        fields = ['title', 'content', 'tags']

        # Widgets about some fields
        widgets = {
            'content': PagedownWidget(
                css=("core/css/markdown.css"),
                show_preview=False
            ),
        }