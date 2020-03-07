from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('register/', views.register.as_view(),name='script'),
    path('video/',views.video_feed,name='video'),
    path('login/', views.login.as_view(),name='check'),
    path('',views.begin.as_view(),name='begin'),
    #path('^/(?P<stream_path>(.*?))/$',views.dynamic_stream,name='videostream'),
    #path('stream/',views.indexscreen),

]