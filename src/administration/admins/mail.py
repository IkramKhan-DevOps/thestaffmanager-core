from django.core.mail import EmailMessage
from core.settings import EMAIL_HOST_USER


def sent_email_over_employee_create(title, body, recipient):
    results = EmailMessage(
        title,
        body,
        EMAIL_HOST_USER,
        [recipient],
    )
    print(results.send())
