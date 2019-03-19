from django.db import models


#
class Mails(models.Model):
    sent_to = models.CharField(max_length=200)
    cc = models.CharField(max_length=200)
    bcc = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    sent_time = models.DateTimeField('date published')

    def __str__(self):
        return self.sent_to
