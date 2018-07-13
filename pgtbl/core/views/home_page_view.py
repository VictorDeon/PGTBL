from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.conf import settings

# Core app
from core.email import send_email_template
from core.generics import FormListView
from core.forms import SendEmailForm
from core.models import News


class HomePageView(FormListView):
    """
    Home page of application.
    """

    template_name = 'home/home.html'
    context_object_name = 'news_list'

    # Get the SendEmailForm
    form_class = SendEmailForm

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def get_queryset(self):
        """
        Get the last two news from queryset database
        """

        queryset = News.objects.all()[:2]

        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        # Get the initial context from IndexView (paginator, page_obj,
        # is_paginated, context_object_name especify or object_list)
        context = super(HomePageView, self).get_context_data()
        # Insert home and logged variables to template
        context['home'] = True
        return context

    def form_valid(self, form):
        """
        Validated email fields and send email.
        """

        # Send email to admin
        send_email_template(
            subject=_("PGTBL - message from {0}"
                      .format(form.cleaned_data['name'])
                      ),
            template='core/email.html',
            from_email=form.cleaned_data['email'],
            context={
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            },
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        messages.success(
            self.request,
            _("Message sent successfully.")
        )

        # Redirect to success_url
        return super(HomePageView, self).form_valid(form)
