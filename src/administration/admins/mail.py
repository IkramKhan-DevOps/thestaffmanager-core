from django.core.mail import EmailMessage, EmailMultiAlternatives
from core.settings import EMAIL_HOST_USER


def sent_email_over_employee_create(recipient):
    try:
        addresses = [recipient]

        subject = 'Employee Account Created'
        from_email = EMAIL_HOST_USER
        to = recipient.email
        text_content = 'Welcome to the Staff Manager'
        html_content = f'<p>Hi <b>{recipient.username}</b> you have been registered as ' \
                       f'an employee by administartion of <b>thestaffmanager.com</b></p>' \
                       f'<p>username: {recipient.username}</p>' \
                       f'<p>email: {recipient.email}</p>' \
                       f'<p>password: 1100@0011{recipient.username}0011@0011</p>'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        EmailMessage(
            subject,
            html_content,
            EMAIL_HOST_USER,
            addresses,
        )
        return True
    except Exception as e:
        print(e)
        return False
