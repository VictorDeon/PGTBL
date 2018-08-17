from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from grades.models import Grade
from groups.models import Group
from modules.models import TBLSession
from peer_review.forms import PeerReviewForm
from peer_review.models import PeerReviewSubmission


class PeerReviewUpdateView(LoginRequiredMixin,
                           PermissionMixin,
                           UpdateView):
    """
    Update the Pair Review available and weight
    """

    model = TBLSession
    template_name = "peer_review/peer_review.html"
    form_class = PeerReviewForm

    permissions_required = ['crud_peer_review']

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        failure_redirect_path = reverse_lazy(
            'modules:details',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return failure_redirect_path

    def get_discipline(self):
        """
        Get the specific discipline

        :return Discipline:
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Get the specific session

        :return: TBLSession
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_success_url(self):
        """
        Get success url to redirect.

        :return String:
        """

        success_url = reverse_lazy(
            'peer_review:list',
            kwargs={
                'slug': self.kwargs.get('slug', ''),
                'pk': self.kwargs.get('pk', '')
            }
        )

        return success_url

    def form_valid(self, form):
        """
        Return the form with fields valided.

        :param form:
        :return HttpResponseRedirect:
        """

        discipline = self.get_discipline()

        if not form['peer_review_available'].value():
            for student in discipline.students.all():
                peer_review_grade = self.calcule_peer_review_grade(student)
                self.update_grade(student, peer_review_grade)

        messages.success(self.request, _("Pair Review updated successfully."))

        return super(PeerReviewUpdateView, self).form_valid(form)

    def calcule_peer_review_grade(self, student):
        """
        Calcule the peer review grade of session students

        :param form: Form to verify if peer review is closed
        """

        peer_review_grade = 0

        submissions = PeerReviewSubmission.objects.filter(
            session=self.get_session(),
            student=student
        )

        for submission in submissions:
            peer_review_grade += submission.score

        group = self.get_student_group(student)
        group_length = group.students.count() - 1

        peer_review_grade = (peer_review_grade / group_length) / 10

        return peer_review_grade

    def get_student_group(self, student):
        """
        Get the student group length

        :return: Group length
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if student in group.students.all():
                return group

    def update_grade(self, student, peer_review_grade):
        """
        Update the student grade with peer review grade.

        :param student: Student grade to be updated
        :param peer_review_grade: Peer Review grade
        """

        try:
            grade = Grade.objects.get(
                session=self.get_session(),
                student=student
            )

            grade.peer_review = peer_review_grade
            grade.save()
        except:
            Grade.objects.create(
                session=self.get_session(),
                student=student,
                group=self.get_student_group(student),
                peer_review=peer_review_grade
            )