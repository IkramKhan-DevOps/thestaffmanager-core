from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core.settings import EMAIL_HOST_USER


def sent_email_over_employee_create(recipient, password):
    try:
        to_list = [recipient.email]
        context = {
            'org': 'National FM Services',
            'tagline': 'National FM Services LTD',
            'link': 'https://nationalfmservices.co,uk',
            'login_link': 'https://nationalfmservices.thestaffmanager.com/accounts/login/',
            'username': recipient.username,
            'email': recipient.email,
            'password': password

        }
        html_message = render_to_string(template_name="emails/employee_registration.html", context=context)
        subject = 'Employee Account Created'
        from_email = EMAIL_HOST_USER

        message = EmailMessage(subject, html_message, from_email, to_list)
        message.content_subtype = 'html'
        message.send()

    except Exception as e:
        return False, e

    return True, None
