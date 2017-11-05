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
    """
    Function to send email.
    """

    # Generate the html template message in string form
    message_html = render_to_string(template, context)

    # Generate the text message from html removing html tags
    message_txt = strip_tags(message_html)

    # Create the email with multiple alternatives to render html if it can
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=recipient_list
    )

    # If the email reader accepts the html form as an alternative, use it
    email.attach_alternative(message_html, "text/html")

    # When email sending fails, it will silently throw an exception or not
    email.send(fail_silently=fail_silently)
