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
    path('detailuser/',views.detailuser,name='detailuser'),

    #-------book------#
    path('nhapsach/',views.input_book.as_view(),name='nhapsach'),
    #path('listbook/',views.list_book,name='listbook'),
    path('detailbook/<int:id>/',views.detailbook,name='detailbook'),
    #path('addcart/',views.addcart,name='addcart'),
    #path('yourcart/',views.yourcart.as_view(),name='yourcart'),

    path('checkbook/',views.check_book,name='checkbook'),
    path('test/',views.testcheck,name='testcheck'),
    path('book/',views.book,name='book'),
    path('book_giaotrinh/',views.book_cate1,name='cate1'),
    path('book_vanhoc/',views.book_cate2,name='cate2'),
    path('book_tamly/',views.book_cate3,name='cate3'),
    path('book_truyen/',views.book_cate4,name='cate4'),
    path('book_vanhoa/',views.book_cate5,name='cate5'),
    path('book_khcn/',views.book_cate6,name='cate6'),
    path('book_chinhtri/',views.book_cate7,name='cate7'),


    #-----mượn trả ------ #
    path('scan_muon/', views.scan_id, name='scan_muon'),
    path('scan_tra/', views.scan_id, name='scan_tra'),
    path('muonsach/', views.bor_book.as_view(), name='muonsach'),
    path('trasach/', views.ret_book.as_view(), name='trasach'),
    path('thanhtoan/', views.thanhtoan.as_view(), name='thanhtoan'),

    #-----contact------#
    path('contact/',views.contact.as_view(),name='contact'),
]