from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'mammo'

urlpatterns = [
    url(r'^$', views.MammoHome, name="mammo_home"),
    url(r'^upload-mammo/$', views.uploadMammo, name="upload_Mammo"),
    url(r'^predictMammo/$', views.predictMammo, name="predictMammo")
]
