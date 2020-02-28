from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('register/',views.register.as_view(),name='register'),
    path('register_button/', views.but_register.as_view(),name='script'),
    path('video/',views.video_feed,name='video'),
    path('login/',views.login.as_view()),
    path('login_button/', views.but_login.as_view(),name='check'),
    path('login_cam/',views.video_cam_recog,name='cam_recog'),

    #path('^/(?P<stream_path>(.*?))/$',views.dynamic_stream,name='videostream'),
    #path('stream/',views.indexscreen),

]