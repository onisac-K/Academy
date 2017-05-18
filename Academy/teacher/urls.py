from django.conf.urls import url
from teacher import views

urlpatterns = [
    url(r'^teacher/$',views.teacher,name = 'teacher'),
    url(r'^score/$',views.teacher,name = 'score'),
]
