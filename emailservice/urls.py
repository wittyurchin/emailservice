from django.urls import path

from . import views

app_name = 'emailservice'

urlpatterns = [
    path('', views.index, name='index'),
    path('sendmail/', views.sendmail, name='sendmail'),
    path('csvupload/', views.csvupload, name='csvupload'),
    path('upload/', views.upload, name='upload'),

]
