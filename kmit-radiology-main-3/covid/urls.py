from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'covid'

urlpatterns = [
    url(r'^$', views.CovidHome, name="covid_home"),
    url(r'^upload_covid/$', views.uploadCovid, name="upload_covid"),
    url(r'^predictCovid/$', views.predictCovid, name="predict_covid"),
    url(r'^showCovid/$', views.showCovid, name="show_covid"),
    url(r'^getCovitCT/$', views.getCovidList, name="list_covid"),
    url(r'^sent/$', views.sentImage, name="sent_Image")
    # url(r'^fileupload/$', views.uploadToServer, name="upload_server")
]
