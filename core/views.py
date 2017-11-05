# Django app
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

# Core app
from .email import send_email_template
from .generics import FormListView
from .forms import SendEmailForm
from .models import News


class HomePageView(FormListView):
    """
    Home page of application.
    """

    template_name = 'core/home.html'
    context_object_name = 'news_list'

    # Use SendEmailForm
    form_class = SendEmailForm

    # Redirect to home page
    success_url = reverse_lazy('core:home')

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        # Get the last two news created
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


class NewsListView(ListView):
    paginate_by = 6
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        """
        Get the specific queryset from model database.
        """

        queryset = News.objects.all()
        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')
        if tag:
            # Verify if the tag url slug contains the specific tag and get all
            # elemente with that tag
            queryset = queryset.filter(tags__slug__icontains=tag)
        # return searched news
        queryset = self.search_news(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Insert more elements into context data to template.
        """

        context = super(NewsListView, self).get_context_data()
        context['home'] = False
        # Get the tag by key argument from url
        tag = self.kwargs.get('tag', '')
        if tag:
            context['tag'] = tag
        return context

    def search_news(self, news_list):
        """
        Search from news list the specific news
        """

        query = self.request.GET.get("q_info")
        if query:
            # Verify if news title and content contains the query specify
            # by user and filter all news that satisfies this
            news_list = news_list.filter(
                            Q(title__icontains=query) |
                            Q(content__icontains=query)
                        ).distinct()
        return news_list


class NewsDetailView(DetailView):
    model = News
    template_name = 'core/news_details.html'
