from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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

    def sum_of_scores(self, form1, form2, form3, form4, form5):
        scores = int(self.return_score(form1)) + \
                 int(self.return_score(form2)) + \
                 int(self.return_score(form3)) + \
                 int(self.return_score(form4)) + \
                 int(self.return_score(form5))

        if scores == 100:
            return False

        return True

    def return_score(self, form):
        if form.is_valid():
            return form.cleaned_data['score']
        else:
            return 0

    def form_validation(self, form, count, index):
        if count > index:
            if form.is_valid():
                self.form_valid(form, index+1)
            else:
                return self.form_invalid(form)


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        discipline = self.get_discipline()
        students = self.get_all_students(discipline)
        session = self.get_session()

        form1 = Student1Form(request.POST, prefix='student1')
        form2 = Student2Form(request.POST, prefix='student2')
        form3 = Student3Form(request.POST, prefix='student3')
        form4 = Student4Form(request.POST, prefix='student4')
        form5 = Student5Form(request.POST, prefix='student5')

        if self.sum_of_scores(form1, form2, form3, form4, form5):
            messages.error(request, 'Make sure the sum of scores is 100')

        else:

            self.form_validation(form1, students.count(), 0)
            self.form_validation(form2, students.count(), 1)
            self.form_validation(form3, students.count(), 2)
            self.form_validation(form4, students.count(), 3)
            self.form_validation(form5, students.count(), 4)

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

    def return_existent_form_data(self, username_gave, username_received, session):

        """
        Check if review already exists
        """
        try:
            # peer_review = get_object_or_404(PeerReview,
            #                                 username_gave=username_gave,
            #                                 username_received=username_received,
            #                                 session=session)

            query = PeerReview.objects.get(
                username_gave=username_gave,
                username_received=username_received,
                session=session,
            )
            peer_review = query

            if peer_review.score is not None:
                data = {'score': peer_review.score,
                        'feedback': peer_review.feedback}
            else:
                data = None
        except PeerReview.DoesNotExist:
            data = None

        return data

    def get_form_data(self, peer_review):
        if peer_review.score is not None:
            data = {'score': peer_review.score,
                    'feedback': peer_review.feedback}
        else:
            data = None

        return data

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
        session = self.get_session()
        students = self.get_all_students(discipline)

        i = 1
        for student in students:
            if i == 1:
                context['student1'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form1'] = Student1Form(initial=self.get_form_data(peer_review), prefix='student1')
            elif i == 2:
                context['student2'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form2'] = Student2Form(initial=self.get_form_data(peer_review), prefix='student2')
            elif i == 3:
                context['student3'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form3'] = Student3Form(initial=self.get_form_data(peer_review), prefix='student3')
            elif i == 4:
                context['student4'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form4'] = Student4Form(initial=self.get_form_data(peer_review), prefix='student4')
            elif i == 5:
                context['student5'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form5'] = Student5Form(initial=self.get_form_data(peer_review), prefix='student5')
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
