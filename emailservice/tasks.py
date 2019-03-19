from __future__ import absolute_import, unicode_literals

import os
from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'artivatic.settings'
application = get_wsgi_application()

import csv


# Create your tasks here
from celery import shared_task
from celery.utils.log import get_task_logger
from emailservice.models import Mails
from datetime import date
from io import StringIO
from artivatic import settings
from emailservice.sendemail import SendEmail
logger = get_task_logger(__name__)



@shared_task
def send_emails_list(emails):
    logger.info("csv mail task initiated")
    for email in emails:
        # print (email)
        SendEmail().sendmail_csv_single(email)


@shared_task
def send_email_form(to_email, cc, bcc, subject, emailbody):
    logger.info("Mail from from is about to be sent")
    SendEmail().sendmailform(to_email, cc, bcc, subject, emailbody)


@shared_task
def test_task():
    print("hello world")


@shared_task
def admin_mail():
    logger.info("Sending recurring mail with mail logs to admin")
    admin_email_id = settings.ADMINS[0][1]
    mails = Mails.objects.filter(sent_time__date=date.today())
    email_ids = [mail.sent_to for mail in mails]
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    for email in email_ids:
        csvwriter.writerow([email])
    # SendEmail().sendmail_attachment()
    SendEmail().sendmail_attachment([admin_email_id], [], [], "Mail report", "Report has been attached", csvfile)

if __name__ == '__main__':
    # from django.conf import settings  # noqa

    admin_mail()