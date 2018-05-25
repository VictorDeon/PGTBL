# Django imports
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import (
    CreateView, ListView, UpdateView, FormView, DeleteView
)

# Application imoports
from disciplines.models import Discipline
from core.email import send_email_template
from core.utils import generate_hash_key
from .forms import UserCreationForm, PasswordResetForm
from .models import PasswordReset

# Get the custom user from settings
User = get_user_model()


class ProfileView(LoginRequiredMixin, ListView):
    """
    Class to read a profile user and his disciplines.
    """

    paginate_by = 6
    template_name = 'accounts/profile.html'
    context_object_name = 'disciplines'

    def get_queryset(self):
        """
        If user is a student get the disciplines that he is taking
        If user is a teacher get the created disciplines and disciplines
        that he is monitor
        """

        queryset = self.filter_student_disciplines()

        if self.request.user.is_teacher:
            queryset = self.filter_teacher_disciplines()

        return queryset

    def filter_teacher_disciplines(self):
        """
        Get disciplines that teacher created or is a monitor.
        """

        created_disciplines = Discipline.objects.filter(
            teacher=self.request.user
        )

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        # Join the created disciplines list and monitor disciplines list
        queryset = []
        for discipline in created_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        # Get the filter by key argument from url
        filtered = self.request.GET.get('filter')

        if filtered == 'created':
            queryset = created_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset

    def filter_student_disciplines(self):
        """
        Get the students disciplines that he is taking
        """

        student_disciplines = Discipline.objects.filter(
            students=self.request.user
        )

        monitor_disciplines = Discipline.objects.filter(
            monitors=self.request.user
        )

        queryset = []
        for discipline in student_disciplines:
            queryset.append(discipline)

        for discipline in monitor_disciplines:
            queryset.append(discipline)

        # Get the filter by key argument from url
        filtered = self.request.GET.get('filter')

        if filtered == 'student':
            queryset = student_disciplines
        elif filtered == 'monitor':
            queryset = monitor_disciplines

        return queryset


class RegisterView(CreateView):
    """
    Class to create a new user.
    """

    model = User
    template_name = 'accounts/register.html'
    form_class = UserCreationForm

    # Redirect to profile
    success_url = reverse_lazy('accounts:profile')



    def form_valid(self, form):
        """
        Receive the form already validated.
        Logs the user into the system.
        """

        # Get the user saved by form.
        user = form.save()

        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        if user.is_teacher:
            messages.success(
                self.request,
                _("Teacher created successfully.")
            )
        else:
            messages.success(
                self.request,
                _("Student created successfully.")
            )

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

    def form_valid(self, form):
        """
        Get the form validated, send successfully message and return the
        success_url.
        """

        messages.success(
            self.request,
            _("User updated successfully.")
        )

        # Redirect to success_url
        return super(EditProfileView, self).form_valid(form)


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    """
    Delete the user account
    """

    model = User

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def get_object(self):
        """
        Search a ID or slug from url and return a object from model.
        In this case return the current user logged from model.
        """

        return self.request.user

    def get_success_url(self):
        """
        Redirect to success_url and show a message.
        """

        messages.success(self.request, _("Account deleted successfully."))

        # Redirect to success_url
        return super(DeleteProfileView, self).get_success_url()


class EditPasswordView(LoginRequiredMixin, FormView):
    """
    Edit user password.
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

        # Get the kwargs from the original class FormView
        kwargs = super(EditPasswordView, self).get_form_kwargs()

        # Insert the parameter logged user into the form template
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Receive the form already validated.
        """

        # In this case when you insert new kwargs, you need to save
        # the instance again
        form.save()

        messages.success(self.request, _("Password updated successfully."))

        # Redirect to success_url
        return super(EditPasswordView, self).form_valid(form)


class ResetPasswordView(FormView):
    """
    Reset the user password and send email.
    """

    template_name = 'accounts/reset_password.html'

    # Use the PasswordResetForm
    form_class = PasswordResetForm

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        """
        Validated form and send email.
        """

        user = User.objects.get(email=form.cleaned_data['email'])

        # Generate unique key to reset password
        key = generate_hash_key(user.username)
        reset_password = PasswordReset(user=user, key=key)
        reset_password.save()

        # Send email
        send_email_template(
            subject=_('Requesting new password'),
            template='accounts/reset_password_email.html',
            context={'reset_password': reset_password},
            recipient_list=[user.email],
        )

        messages.success(
            self.request,
            _("An email was sent with more details on how to create a new password")
        )

        # Redirect to success_url
        return super(ResetPasswordView, self).form_valid(form)


class ResetPasswordConfirmView(FormView):
    """
    Insert new password from email link.
    """

    template_name = 'accounts/reset_password_confirm.html'

    # Use SetPasswordForm from django
    form_class = SetPasswordForm

    # Redirect to login page.
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        """
        Insert arguments inside form.
        """

        # Get all arguments kwargs from SetPasswordForm
        kwargs = super(ResetPasswordConfirmView, self).get_form_kwargs()

        # Get the user with kwargs key to reset his password
        reset = get_object_or_404(
            PasswordReset,
            key=self.kwargs.get('key')
        )

        # Change user and data from form
        kwargs['user'] = reset.user
        kwargs['data'] = self.request.POST or None

        return kwargs

    def form_valid(self, form):
        """
        Validated form and reset password.
        """

        # In this case when you insert new kwargs, you need to save
        # the instance again
        form.save()

        messages.success(
            self.request,
            _("Your password was updated successfully.")
        )

        # Redirect to success_url
        return super(ResetPasswordConfirmView, self).form_valid(form)
