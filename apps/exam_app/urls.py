from django.conf.urls import url
from . import views

app_name='exam_app'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.log_register, name="register"),
    url(r'^login$', views.log_register, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^travel$', views.travel, name="travel"),
    url(r'^addtravel$', views.addtravel, name="addtravel"),
    url(r'^add$', views.add, name="add"),
    url(r'^join/(?P<id>\d+)$', views.join, name="join"),
    url(r'^destination/(?P<id>\d+)$', views.destination, name="destination"),
]
'exam_app:index'
'exam_app:register'
'exam_app:login'
'exam_app:logout'
'exam_app:travel'
'exam_app:add'
'exam_app:addtravel'
'exam_app:join'
'exam_app:destination'
