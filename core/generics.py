"""
File to generate new generic views.
"""

from django.utils.translation import ugettext as _
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import redirect
from django.http import Http404


class FormListView(FormMixin, ListView):
    """
    List view with a form.
    """

    def get(self, request, *args, **kwargs):
        """
        Method GET with a POST form.
        """

        # Get the object_list from queryset
        self.object_list = self.get_queryset()
        self.form = None

        # Get the form from form_class
        if self.form_class:
            self.form = self.get_form()

        # Insert object_list and form into template
        self.get_context_data(
            object_list=self.object_list,
            form=self.form
        )

        # Verify if the object list is empty or not when not allow empty list
        # If allow_empty is False will display error 404
        # If allow_empty if True will display the empty template.
        # The default value is True
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            self.cheap_query(allow_empty)

        # Verify if form is valid and call the respective method.
        if self.form:
            return self.form_validation()
            ation()
        else:
            return self.post_validation()

    def form_validation(self):
        """
        Forwards to the correct method depending on the form request.
        """

        if self.form.is_valid():
            return self.form_valid(self.form)

        return self.form_invalid(self.form)

    def post_validation(self):
        """
        Redirect if method is post and render otherwise.
        """

        if self.request.POST:
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=self.form))

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


class FormDetailView(FormMixin, DetailView):
    """
    Detail view with form.
    """

    model = None
    queryset = None
    form_class = None
    success_url = None
    template_name = None
    context_object_name = None
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

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

    def get(self, request, *args, **kwargs):
        """
        Method get with form.
        """

        self.form = None

        # Get the form from form_class
        if self.form_class:
            self.form = self.get_form()

        # Get the object from queryset
        self.object = self.get_object()

        # Verify if form is valid and call the respective method.
        if self.form:
            return self.form_validation()
        else:
            return self.post_validation()

    def form_validation(self):
        """
        Forwards to the correct method depending on the form request.
        """

        if self.form.is_valid():
            return self.form_valid(self.form)

        return self.form_invalid(self.form)

    def post_validation(self):
        """
        Redirect if method is post and render otherwise.
        """

        if self.request.POST:
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=self.form))


class ObjectRedirectView(DeleteView):
    """
    Redirect to success url after perform some action.
    """

    def post(self, request, *args, **kwargs):
        """
        Post method to perform some action.
        """

        return self.action(request, *args, **kwargs)

    def action(self, request, *args, **kwargs):
        """
        Do some action.
        """

        self.object = self.get_object()
        success_url = self.get_success_url()
        return redirect(success_url)
