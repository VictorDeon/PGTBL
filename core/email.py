from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email_template(subject,
                        template,
                        context,
                        recipient_list,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        fail_silently=False):

    message_html = render_to_string(template, context)
    message_txt = strip_tags(message_html)
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)
