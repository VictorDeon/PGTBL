from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import (
    FormView
)

# Application imports
from TBLSessions.models import TBLSession
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from peer_review.models import PeerReview
from .forms import Student1Form, Student2Form, Student3Form, Student4Form, Student5Form

# Get the custom user from settings
User = get_user_model()


class PeerReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     FormView):
    """
    Working with form to create a peer review
    """

    template_name = 'peer_review/peer.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = Student1Form
    permissions_required = [
        'only_student_can_change'
    ]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        discipline = self.get_discipline()
        students = self.get_all_students(discipline)

        form1 = Student1Form(request.POST, prefix='student1')
        form2 = Student2Form(request.POST, prefix='student2')
        form3 = Student3Form(request.POST, prefix='student3')
        form4 = Student4Form(request.POST, prefix='student4')
        form5 = Student5Form(request.POST, prefix='student5')

        if students.count() > 0:
            if form1.is_valid():
                self.form_valid(form1, 1)
            else:
                messages.info(request, 'Your first form is invalid!')
                return self.form_invalid(form1)

        if students.count() > 1:
            if form2.is_valid():
                self.form_valid(form2, 2)
            else:
                messages.info(request, 'Your second form is invalid!')
                return self.form_invalid(form2)

        if students.count() > 2:
            if form3.is_valid():
                self.form_valid(form3, 3)
            else:
                messages.info(request, 'Your third form is invalid!')
                return self.form_invalid(form3)

        if students.count() > 3:
            if form4.is_valid():
                self.form_valid(form4, 4)
            else:
                messages.info(request, 'Your fourth form is invalid!')
                return self.form_invalid(form4)

        if students.count() > 4:
            if form5.is_valid():
                self.form_valid(form5, 5)
            else:
                messages.info(request, 'Your fifth form is invalid!')
                return self.form_invalid(form5)

        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form, student_index):

        """
        Receive the form already validated to create an Peer Review
        """
        discipline = self.get_discipline()
        students = self.get_all_students(discipline)
        session = self.get_session().id

        i = 1
        for student in students:
            if i == student_index:
                username_gave = self.request.user.get_full_name()
                username_received = student.get_full_name()

                peer_review = self.return_existent_review(username_gave, username_received, session)

                peer_review.username_gave = username_gave
                peer_review.username_received = username_received
                peer_review.session = session
                peer_review.feedback = form.cleaned_data.get('feedback')

                if form.cleaned_data.get('score') is None:
                    peer_review.score = 0
                else:
                    peer_review.score = form.cleaned_data.get('score')
                peer_review.save()
            i += 1

    def return_existent_review(self, username_gave, username_received, session):

        """
        Check if peer review already exists
        """

        try:
            query = PeerReview.objects.get(
                username_gave=username_gave,
                username_received=username_received,
                session=session,
            )
            peer_review = query
        except PeerReview.DoesNotExist:
            peer_review = PeerReview()

        return peer_review

    def get_context_data(self, **kwargs):
        context = super(PeerReviewView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['student1'] = None
        context['student2'] = None
        context['student3'] = None
        context['student4'] = None
        context['student5'] = None

        discipline = self.get_discipline()
        students = self.get_all_students(discipline)

        i = 1
        for student in students:
            if i == 1:
                context['student1'] = student
                context['form1'] = Student1Form(prefix='student1')
            elif i == 2:
                context['student2'] = student
                context['form2'] = Student2Form(prefix='student2')
            elif i == 3:
                context['student3'] = student
                context['form3'] = Student3Form(prefix='student3')
            elif i == 4:
                context['student4'] = student
                context['form4'] = Student4Form(prefix='student4')
            elif i == 5:
                context['student5'] = student
                context['form5'] = Student5Form(prefix='student5')
            i += 1

        return context

    def get_discipline(self):
        """
        Get the specific discipline.
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the group belongs to
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_all_students(self, discipline):
        """
        Get students from dicipline except the current user
        """
        user_logged_in = self.get_user_logged_in()
        students = discipline.students.exclude(email=user_logged_in.email)

        return students

    def get_user_logged_in(self):
        user_logged_in = None
        if self.request.user.is_authenticated():
            user_logged_in = self.request.user

        return user_logged_in
