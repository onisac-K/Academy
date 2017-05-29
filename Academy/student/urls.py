from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$',views.student,name = 'student'),
    url(r'^selection$', views.select),
    url(r'^student$', views.student),
    url(r'^drop$', views.drop),
    url(r'^grade$', views.grade),
]
