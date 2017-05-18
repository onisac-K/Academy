from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^student/$',views.student,name = 'student'),
    url(r'^student/select$', views.select),
]
