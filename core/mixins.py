"""
File to create decorator mixins
"""
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.http import Http404


class UserCheckMixin(object):
    """
    Checks a user condition and if this condition is not
    satisfied redirects to a specific url
    """

    user_check_failure_path = ''

    def check_user(self, user):
        """
        If not override return always true.
        """

        return True

    def user_check_failed(self, request, *args, **kwargs):
        """
        If user check fail, redirect the user to another place.
        """

        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        """
        Try to dispatch to the right method.
        """

        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)

        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(UserCheckMixin):
    """
    Insert a permission in one class based view.
    """

    user_check_failure_path = reverse_lazy('accounts:login')
    permission_required = None

    def check_user(self, user):
        """
        Verify if user has specific permission
        """

        return user.has_perm(self.permission_required)


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
        Method POST with GET.
        """

        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Method PUT with GET
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
    Details view with form.
    """

    pass
