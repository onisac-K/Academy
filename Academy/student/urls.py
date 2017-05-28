from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$',views.student,name = 'student'),
    url(r'^selection$', views.select),
    url(r'^delete$', views.delete),
]
