# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import (FormView, ListView, UpdateView)

# Application imports
from TBLSessions.models import TBLSession
from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grades.models import Grade
from groups.models import Group
from peer_review.models import PeerReview
from .forms import StudentForm, PeerReviewUpdateForm, PeerReviewDateForm

# Get the custom user from settings
User = get_user_model()


class PeerReviewView(LoginRequiredMixin,
                     PermissionMixin,
                     FormView):
    """
    Working with form to create a peer review
    """

    template_name = 'peer_review/form.html'
    form_class = StudentForm
    permissions_required = [
        'only_student_can_change'
    ]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        forms = {}
        for idx, student in enumerate(self.get_students_except_logged_student()):
            forms[idx] = StudentForm(request.POST, prefix=student.username)

        if self.sum_of_scores(forms):
            messages.error(request, _('Make sure the sum of scores is 100 and you gave feedback to everyone'))
            return HttpResponseRedirect(
                reverse_lazy(
                    'peer_review:review',
                    kwargs={'slug': self.get_discipline().slug, 'pk': self.get_session().id}
                )
            )
        else:
            for idx in forms:
                self.form_validation(forms[idx], idx)

            messages.success(request, _('Your review was saved successfully!'))

            return HttpResponseRedirect(
                reverse_lazy(
                    'TBLSessions:details',
                    kwargs={'slug': self.get_discipline().slug, 'pk': self.get_session().id}
                )
            )

    def form_valid(self, form, idx):
        """
        Receive the form already validated to create an Peer Review
        """
        students = self.get_students_except_logged_student()
        session = self.get_session().id

        for student_idx, student in enumerate(students):
            if idx == student_idx:
                reviewed_by = self.request.user
                student = student

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

        self.calculate_peer_review()

    def sum_of_scores(self, forms):

        scores = 0
        for idx in forms:
            scores += int(self.return_score(forms[idx]))

        if scores == 100:
            return False

        return True

    @classmethod
    def return_score(self, form):
        if form.is_valid():
            return form.cleaned_data['score']
        else:
            return 0

    def form_validation(self, form, idx):
        if form.is_valid():
            self.form_valid(form, idx)
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
        context['group'] = self.get_student_group(self.request.user)
        context['students'] = self.get_students_except_logged_student()

        for idx, student in enumerate(self.get_students_except_logged_student()):
            peer_review = self.return_existent_review(self.request.user, student, self.get_session().id)
            context['form'+str(idx+1)] = StudentForm(initial=self.get_form_data(peer_review), prefix=student.username)

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

    def get_all_students(self):
        """
        Get students from dicipline except the current user
        """
        user_logged_in = self.get_user_logged_in()
        group = self.get_student_group(user_logged_in)

        return group.students.all()

    def get_students_except_logged_student(self):
        """
        Get students from dicipline except the current user
        """
        user_logged_in = self.get_user_logged_in()
        group = self.get_student_group(user_logged_in)

        return group.students.exclude(username=user_logged_in.username)

    def get_user_logged_in(self):
        user_logged_in = None
        if self.request.user.is_authenticated():
            user_logged_in = self.request.user

        return user_logged_in

    def get_groups(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups

    def get_student_group(self, student_wanted):
        """
        Get the group queryset from model database.
        """

        groups = self.get_groups()

        for group in groups:
            users_in_group = Group.objects.get(title=group.title).students.all()
            for student in users_in_group:
                if student == student_wanted:
                    return group

        return None

    def save_peer_review_grade(self, grade, student, session):

        """
        Check if peer review already exists
        """
        try:
            query = Grade.objects.get(
                student=student,
                session=session,
            )
            student_grade = query
            student_grade.updated_at = timezone.localtime(timezone.now())
        except Grade.DoesNotExist:
            student_grade = Grade()
            student_grade.created_at = timezone.localtime(timezone.now())
            student_grade.student = student
            student_grade.session = session
            student_grade.group = self.get_student_group(student)

        student_grade.peer_review = grade

        student_grade.save()

    def calculate_peer_review(self):
        """
        Calculate the final score of the students.
        """
        peer_review_scores = {}
        students = self.get_all_students()

        max_score = 0
        for student in students:
            peer_reviews = PeerReview.objects.filter(reviewed_by=student, session=self.get_session().id)
            if not peer_reviews:
                peer_review_scores[student] = 0
            else:
                peer_reviews = PeerReview.objects.filter(student=student, session=self.get_session().id)
                score = 0
                for peer_review in peer_reviews:
                    score += peer_review.score
                    peer_review_scores[student] = score
                if max_score < score:
                    max_score = score

        for student in students:
            grade = (peer_review_scores[student]*100) / max_score
            self.save_peer_review_grade(round(grade, 1), student, self.get_session())


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

    def get_groups(self):
        """
        Get the group queryset from model database.
        """

        discipline = self.get_discipline()

        groups = Group.objects.filter(discipline=discipline)

        return groups

    def get_all_students(self):
        """
        Get students from dicipline except the student passed
        """
        discipline = self.get_discipline()

        students = discipline.students.all()

        return students

    def get_context_data(self, **kwargs):
        """
        Insert discipline, session end submissions into result context data.
        """
        context = super(PeerReviewResultView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        context['students'] = self.get_all_students()
        context['submissions'] = self.get_queryset()
        context['groups'] = self.get_groups()

        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """
        session = self.get_session()
        submissions = PeerReview.objects.filter(session=session.id)

        if not submissions:
            submissions = None

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


class PeerReviewDateUpdateView(LoginRequiredMixin,
                               PermissionMixin,
                               UpdateView):
    """
    Update the Peer Review datetime.
    """

    model = TBLSession
    template_name = 'peer_review/datetime.html'
    form_class = PeerReviewDateForm
    permissions_required = [
        'monitor_can_change_if_is_teacher'
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
        context = super(PeerReviewDateUpdateView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def form_valid(self, form):
        """
        Return the form with fields valided.
        """
        now = timezone.localtime(timezone.now())

        if form.instance.peer_review_datetime is None:

            messages.error(
                self.request,
                _("Peer Review date must to be filled in.")
            )

            return redirect(self.get_success_url())

        if now > form.instance.peer_review_datetime:

            messages.error(
                self.request,
                _("Peer Review date must to be later than today's date.")
            )

            return redirect(self.get_success_url())

        messages.success(self.request, _('Peer Review date updated successfully.'))

        return super(PeerReviewDateUpdateView, self).form_valid(form)

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
