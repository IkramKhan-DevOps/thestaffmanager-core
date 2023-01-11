from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template, render_to_string
from core.settings import EMAIL_HOST_USER


def sent_email_over_employee_create(recipient):
    try:
        to_list = [recipient.email]
        context = {
            'username': recipient.username,
            'email': recipient.email,
            'password': '1100@0011' + recipient.username + '0011@0011'
        }
        html_message = render_to_string(template_name="emails/employee_registration.html", context=context)
        subject = 'Employee Account Created'
        from_email = EMAIL_HOST_USER

        message = EmailMessage(subject, html_message, from_email, to_list)
        message.content_subtype = 'html'  # this is required because there is no plain text email message
        message.send()

    except Exception as e:
        return False, e

    return True, None
