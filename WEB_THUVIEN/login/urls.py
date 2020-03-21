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
    #-------book------#
    path('nhapsach/',views.input_book.as_view(),name='nhapsach'),
    #path('listbook/',views.list_book,name='listbook'),
    path('listbook/<int:id>/',views.view_book,name='viewbook'),
    #path('addcart/',views.addcart,name='addcart'),
    #path('yourcart/',views.yourcart.as_view(),name='yourcart'),
    path('book/',views.book),
    path('muonsach/',views.scan_id,name='muonsach'),
    path('trasach/',views.trasach,name='trasach'),
    path('scan_muon/',views.bor_book.as_view(),name='scan_sach'),
    path('scan_tra/',views.ret_book.as_view(),name='scan_tra'),
    path('thanhtoan/',views.thanhtoan.as_view(),name='thanhtoan'),
]