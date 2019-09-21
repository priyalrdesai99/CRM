from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path
from customer.views import viewtransactions,changepassword,updateprofile,viewProfile
urlpatterns = [

url(r'^viewpurchases/$',viewtransactions),
url(r'^updatecuspassword/$',changepassword),
url(r'^updatecusprofile/$',updateprofile),
url(r'^viewcusprofile/$',viewProfile),
]

