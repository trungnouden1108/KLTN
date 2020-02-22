from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('register/',views.register.as_view(),name='register'),
    path('register_button/', views.but_register.as_view(),name='script'),
    path('^/(?P<stream_path>(.*?))/$',views.dynamic_stream,name='videostream'),
    path('stream/',views.indexscreen),
]