from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from groups.models import Group
from modules.models import TBLSession
from notification.models import Notification
from peer_review.forms import PeerReviewAnswerForm
from peer_review.models import PeerReviewSubmission

User = get_user_model()


class PeerReviewAnswerView(LoginRequiredMixin,
                           PermissionMixin,
                           FormView):
    """
    Answer the respective Peer Review test.
    """

    template_name = "peer_review/peer_review.html"
    form_class = PeerReviewAnswerForm

    permissions_required = ['send_peer_review']

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
        Get the discipline from url kwargs

        :return: Specific discipline
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        get the session from url kwargs.

        :return: Specific TBL session
        """

        session = TBLSession.objects.get(
            pk=self.kwargs.get('pk', '')
        )

        return session

    def get_student_group(self):
        """
        Get current student group.
        """

        groups = Group.objects.filter(
            discipline=self.get_discipline()
        )

        for group in groups:
            if self.request.user in group.students.all():
                return group

        return None

    def get_student(self):
        """
        Get the student by url kwargs

        :return: Student to be assessed
        """

        student = User.objects.get(pk=self.kwargs.get('student_id', ''))

        return student

    def get_success_url(self):
        """
        After answer the peer review redirect to module details

        :return: Path String
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
        Form to insert student scores and comment

        :param form: Form from form class validated.
        :return: HttpResponseRedirect with the answer
        """

        student = self.get_student()

        success = self.validate_answer(form)

        if success:
            self.create_submission(student, form)

        return super(PeerReviewAnswerView, self).form_valid(form)

    def validate_answer(self, form):
        """
        Verify if score is correct

        :param form: Form with validated score and comment
        :return: True if all conditions is passed and False otherwise.
        """

        # Verify if student is in some group
        if not self.get_student_group():
            messages.error(
                self.request,
                _("Student must be in a group to answer the test.")
            )

            return False

        # Verify if score is valid
        if int(form['score'].value()) < 0 or int(form['score'].value()) > 100:
            messages.error(
                self.request,
                _("You can't insert a score bigger than 100 or less than 0")
            )

            return False

        # Checks if the student has already been evaluated
        submissions = PeerReviewSubmission.objects.filter(
            session=self.get_session(),
            group=self.get_student_group(),
            student=self.get_student(),
            user=self.request.user
        )

        if submissions.count() > 0:
            messages.error(
                self.request,
                _("You already submit a review to this student.")
            )

            return False

        return True

    def create_submission(self, student, form):
        """
        Create a submission with form inputs
        """

        PeerReviewSubmission.objects.create(
            session=self.get_session(),
            score=int(form['score'].value()),
            comment=form['comment'].value(),
            user=self.request.user,
            student=student,
            group=self.get_student_group()
        )

        self.send_message(student, form)

        messages.success(
            self.request,
            _("Peer Review answered successfully.")
        )

    def send_message(self, student, form):
        """
        Send notification about peer review
        """

        discipline = self.get_discipline()
        session = self.get_session()

        Notification.objects.create(
            title=_("Peer Review Anonymously"),
            description=form['comment'].value() + "\nPeer Review Session: " + str(session.title),
            receiver=student,
            discipline=discipline
        )