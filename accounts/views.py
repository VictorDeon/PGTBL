# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView, ListView, UpdateView, FormView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
# Disciplines APP
from disciplines.models import Discipline
# Accounts APP
from .forms import UserCreationForm, PasswordResetForm
from .models import PasswordReset
# Python
from datetime import datetime

# Get the custom user from settings
User = get_user_model()


class ProfileView(LoginRequiredMixin, ListView):
    """
    Class to read a profile user and his disciplines.
    """

    paginate_by = 5
    template_name = 'accounts/profile.html'
    # object queryset name that appears in the templates
    context_object_name = 'disciplines'

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        queryset = Discipline.objects.filter(teacher=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        # Get the initial context from IndexView (paginator, page_obj,
        # is_paginated, context_object_name especify or object_list)
        context = super(ProfileView, self).get_context_data()
        # Insert home and logged variables to template
        context['date'] = datetime.now().date()
        return context


class RegisterView(CreateView):
    """
    Class to create a new user.
    """

    model = User
    template_name = 'accounts/register.html'

    # Generate the UserCreationForm
    form_class = UserCreationForm

    # Redirect to login page only when the url is requested
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        """
        Receive the form already validated.
        Logs the user into the system.
        """

        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Edit personal information from user.
    """

    model = User
    template_name = 'accounts/edit_information.html'

    # Generate the forms with this fields
    fields = ['photo', 'name', 'username', 'email', 'institution', 'course']

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    """
    Delete the user account
    """

    model = User
    success_url = reverse_lazy('core:home')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user


class EditPasswordView(LoginRequiredMixin, FormView):
    """
    Edit password from user.
    """

    template_name = 'accounts/edit_password.html'

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')

    # Generate the PasswordChangeForm from django
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        """
        Generates the arguments that will be passed to the form.
        """

        # Get the get_form_kwargs() from the original class
        # (PasswordChangeForm)
        kwargs = super(EditPasswordView, self).get_form_kwargs()

        # Insert the parameter logged user into the form template
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # When the form is valid save the instance
        form.save()

        # Return to form_valid function from django to finish edition.
        return super(EditPasswordView, self).form_valid(form)


def reset_password(request):
    """
    Reset the user password and send email.
    """

    template = 'accounts/reset_password.html'
    # If you do not send anything in the form you will insert None
    # and de form will not validated (empty form)
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template, context)


def reset_password_confirm(request, key):
    template = 'accounts/reset_password_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template, context)
