# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import (FormView, ListView, UpdateView)

# Application imports
from TBLSessions.models import TBLSession
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from peer_review.models import PeerReview
from .forms import StudentForm, PeerReviewUpdateForm

# Get the custom user from settings
User = get_user_model()


class PeerReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     FormView):
    """
    Working with form to create a peer review
    """

    template_name = 'peer_review/form.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = StudentForm
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
        session = self.get_session()

        form1 = StudentForm(request.POST, prefix='student1')
        form2 = StudentForm(request.POST, prefix='student2')
        form3 = StudentForm(request.POST, prefix='student3')
        form4 = StudentForm(request.POST, prefix='student4')
        form5 = StudentForm(request.POST, prefix='student5')

        if self.sum_of_scores(form1, form2, form3, form4, form5):
            messages.error(request, 'ERROR: Your review was not saved! Make sure the sum of scores is 100')
            return HttpResponseRedirect(reverse_lazy('peer_review:review', kwargs={'slug': discipline.slug, 'pk': session.id}))
        else:

            self.form_validation(form1, students.count(), 0)
            self.form_validation(form2, students.count(), 1)
            self.form_validation(form3, students.count(), 2)
            self.form_validation(form4, students.count(), 3)
            self.form_validation(form5, students.count(), 4)

            messages.success(request, 'Your review was saved successfully!')

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
                reviewed_by = self.request.user.get_full_name()
                student = student.get_full_name()

                peer_review = self.return_existent_review(reviewed_by, student, session)

                peer_review.reviewed_by = reviewed_by
                peer_review.student = student
                peer_review.session = session
                peer_review.feedback = form.cleaned_data.get('feedback')

                if form.cleaned_data.get('score') is None:
                    peer_review.score = 0
                else:
                    peer_review.score = form.cleaned_data.get('score')
                peer_review.save()
            i += 1

    def sum_of_scores(self, form1, form2, form3, form4, form5):
        scores = int(self.return_score(form1)) + \
                 int(self.return_score(form2)) + \
                 int(self.return_score(form3)) + \
                 int(self.return_score(form4)) + \
                 int(self.return_score(form5))

        if scores == 100:
            return False

        return True

    @classmethod
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

    @classmethod
    def return_existent_review(self, reviewed_by, student, session):

        """
        Check if peer review already exists
        """

        try:
            query = PeerReview.objects.get(
                reviewed_by=reviewed_by,
                student=student,
                session=session,
            )
            peer_review = query
        except PeerReview.DoesNotExist:
            peer_review = PeerReview()

        return peer_review

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
                context['form1'] = StudentForm(initial=self.get_form_data(peer_review), prefix='student1')
            elif i == 2:
                context['student2'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form2'] = StudentForm(initial=self.get_form_data(peer_review), prefix='student2')
            elif i == 3:
                context['student3'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form3'] = StudentForm(initial=self.get_form_data(peer_review), prefix='student3')
            elif i == 4:
                context['student4'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form4'] = StudentForm(initial=self.get_form_data(peer_review), prefix='student4')
            elif i == 5:
                context['student5'] = student
                peer_review = self.return_existent_review(self.request.user.get_full_name(),
                                                          student.get_full_name(),
                                                          session.id)
                context['form5'] = StudentForm(initial=self.get_form_data(peer_review), prefix='student5')
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
        students = discipline.students.exclude(username=user_logged_in.username)

        return students

    def get_user_logged_in(self):
        user_logged_in = None
        if self.request.user.is_authenticated():
            user_logged_in = self.request.user

        return user_logged_in


class PeerReviewResultView(LoginRequiredMixin,
                           PermissionMixin,
                           ListView):
    """
    Show the result of Peer Review.
    """

    template_name = 'peer_review/result.html'
    context_object_name = 'submissions'
    permissions_required = [
        'only_teacher_can_change'
    ]

    def get_discipline(self):
        """
        Get the discipline from url kwargs.
        """
        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.
        """
        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_all_students(self, student):
        """
        Get students from dicipline except the student passed
        """
        discipline = self.get_discipline()

        if student is None:
            students = discipline.students.all()
        else:
            students = discipline.students.exclude(username=student.username)

        return students

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session end submissions into result context data.
        """
        context = super(PeerReviewResultView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['submissions'] = self.get_queryset()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """
        session = self.get_session()
        submissions = PeerReview.objects.filter(session=session.id)

        return submissions


class PeerReviewUpdateView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    Update the Peer Review availability and weight
    """
    model = TBLSession
    template_name = 'peer_review/update.html'
    form_class = PeerReviewUpdateForm
    permissions_required = [
        'monitor_can_change_if_is_teacher'
    ]

    def get_discipline(self):
        """
        Take the discipline that the tbl session belongs to
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

    def get_context_data(self, **kwargs):
        """
        Insert a discipline and session inside template.
        """
        context = super(PeerReviewUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valid
        """
        messages.success(self.request, 'Peer Review updated successfully.')

        return super(PeerReviewUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        Get success url to redirect.
        """
        discipline = self.get_discipline()
        session = self.get_session()

        success_url = reverse_lazy(
            'peer_review:result',
            kwargs={'slug': discipline.slug, 'pk': session.id}
        )

        return success_url
