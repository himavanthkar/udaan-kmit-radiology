from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'auths'

urlpatterns = [
    # url(r'^signup/', views.Signup, name="signup"),
    url(r'^login/$', views.Login, name="login"),
    url(r'^logout/$', views.Logout, name = "logout"),
]