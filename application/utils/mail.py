import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configuration import (
    settings,
    logger as setting_logger
)

logger = setting_logger.get_logger(__name__)


def send(email_from, email_to, subject, template, variables={}):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to

    template = settings.jinja_env.get_template(template)
    html = template.render(variables)

    text = "Пожалуйста используйте html версию письма."
    mime_text = MIMEText(text, 'plain')
    html_text = MIMEText(html, 'html')

    msg.attach(mime_text)
    msg.attach(html_text)

    logger.info(f'Send email to {email_to}')

    with smtplib.SMTP_SSL(settings.EMAIL_URL, settings.EMAIL_PORT) as server:
        server.ehlo()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.sendmail(email_from, email_to, msg.as_string())

    logger.info(f'Email to {email_to} sent')
