"""
File to generate new generic views.
"""

from django.utils.translation import ugettext as _
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from django.http import Http404


class FormListView(FormMixin, ListView):
    """
    List view with a form.
    """

    def get(self, request, *args, **kwargs):
        """
        Method GET with a POST form.
        """

        # Get the form from form_class
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # Get the object_list from queryset
        self.object_list = self.get_queryset()

        # Verify if the object list is empty or not when not allow empty list
        # If allow_empty is False will display error 404
        # If allow_empty if True will display the empty template.
        # The default value is True
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            self.cheap_query(allow_empty)

        # Insert object_list and form into template
        context = self.get_context_data(
            object_list=self.object_list,
            form=self.form
        )

        # Verify if form is valid and call the respective method.
        if self.form.is_valid():
            return self.form_valid(self.form)
        else:
            return self.form_invalid(self.form)

        # render the template.
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Method POST in GET.
        """

        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Method PUT in GET
        """

        return self.get(request, *args, **kwargs)

    def cheap_query(self, allow_empty):
        """
        When pagination is enabled and object_list is a queryset,
        it's better to do a cheap query than to load the unpaginated
        queryset in memory.
        """

        pagination_enabled = self.get_paginate_by(self.object_list) is not None
        object_list_is_queryset = hasattr(self.object_list, 'exists')

        if pagination_enabled and object_list_is_queryset:
            is_empty = not self.object_list.exists()
        else:
            is_empty = len(self.object_list) == 0

        if is_empty:
            raise Http404(
                _(u"Empty list and {class_name}.allow_empty is False.")
                .format(class_name=self.__class__.__name__)
            )
