import csv
# from django.http import HttpResponse,HttpResponseRedirect
# from .models import Choice, Question
import logging
import os
import string

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .csvutil import getemailids
from .tasks import send_emails_list, send_email_form

logger = logging.getLogger(__name__)


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    context = {}
    return render(request, 'emailservice/index.html', context)


def sendmail(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        # print(form_data)
        to_email = form_data.get("email")
        cc = form_data.get("cc")
        bcc = form_data.get("bcc")
        subject = form_data.get("subject")
        emailbody = form_data.get("emailbody")
        r = send_email_form.delay(to_email, cc, bcc, subject, emailbody)
        logger.info("A mail has been sent using the form:-" + str(form_data))
        return render(request, 'emailservice/email_success.html', {})
    return render(request, 'emailservice/index.html', {})


def csvupload(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    context = {}
    return render(request, 'emailservice/csvupload.html', context)


#
def upload(request):
    print(request.FILES)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if not is_csv(uploaded_file_url):
            if os.path.exists(uploaded_file_url):
                os.remove(uploaded_file_url)
            else:
                print("what happened?")
            context = {'error_message': "Not a valid csv file"}
            return render(request, 'emailservice/index.html', context)
        emailids = getemailids(uploaded_file_url)
        r = send_emails_list.delay(emailids)
        return render(request, 'emailservice/upload_success.html', {
            'uploaded_file_url': uploaded_file_url
        })
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return render(request, 'emailservice/csvupload.html', {})


def is_textfile(file_name):
    try:
        with open(file_name, 'tr') as check_file:  # try open file in text mode
            check_file.read()
            return True
    except:  # if fail then file is non-text (binary)
        return False


def is_csv(infile):
    if not is_textfile(infile):
        print("not text file")
        return False
    try:
        print("A text file")
        with open(infile, newline='') as csvfile:
            start = csvfile.read(4096)

            # isprintable does not allow newlines, printable does not allow umlauts...
            if not all([c in string.printable or c.isprintable() for c in start]):
                return False
            dialect = csv.Sniffer().sniff(start)
            return True
    except csv.Error as e:
        # Could not get a csv dialect -> probably not a csv.
        print(e)
        return False
