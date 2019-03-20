import smtplib
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
# from emailservice.models import MailLogs
from django.utils import timezone
from django.conf import settings
import os
import logging

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artivatic.settings')
from artivatic import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from artivatic.settings import BASE_DIR
from emailservice.models import Mails

module_logger = logging.getLogger('artivatic.sendemail')


class SendEmail:
    MY_ADDRESS = settings.DEFAULT_FROM_EMAIL

    def __init__(self):
        self.logger = logging.getLogger('artivatic.sendemail.SendEmail')
        self.logger.info('creating SendEmail')

    def read_template(self, filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def sendmail_csv_single(self, to_email):
        file_path = os.path.join(BASE_DIR, 'artivatic/emailservice/email_message_template.txt')
        message_template = self.read_template(
            file_path)
        # add in the actual person name to the message template
        emailbody = message_template.substitute(PERSON_NAME=to_email)
        self.sendmail([to_email], [], [], "subject", emailbody)

    def sendmailform(self, to_email, cc, bcc, subject, emailbody):
        self.sendmail([to_email], [cc], [bcc], subject, emailbody)

    def sendmail(self, to_email, cc, bcc, subject, emailbody):
        q = Mails(sent_to=' , '.join(to_email), cc=' , '.join(cc), bcc=' , '.join(bcc), subject=subject, body=emailbody,
                  sent_time=timezone.now())
        q.save()
        self.logger.info("A mail has been sent. " + str(q.id))
        message = EmailMultiAlternatives(subject, emailbody, SendEmail.MY_ADDRESS, to=to_email, bcc=bcc, cc=cc)
        message.send(fail_silently=False)

    def sendmail_attachment(self, to_email, cc, bcc, subject, emailbody, csvfile):
        message = EmailMultiAlternatives(subject, emailbody, SendEmail.MY_ADDRESS, to=to_email, bcc=bcc, cc=cc)
        message.attach('emailreport.csv', csvfile.getvalue(), 'text/csv')
        message.send(fail_silently=False)
        self.logger.info("Admin mail has been sent. To- "+to_email[0])


if __name__ == '__main__':
    # sendmail_single("purna.patro@gmail.com")
    # logger = logging.getLogger("whats my name")
    # logger.setLevel(logging.INFO)
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)
    # logger.info('creating an instance of auxiliary_module.Auxiliary')
    s = SendEmail()
    s.sendmailform("purna.patro@gmail.com", "hello", "hello", "hello", "hello")
