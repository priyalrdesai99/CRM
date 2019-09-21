from crmapp.views import auth_view,login,logout,invalidlogin,loggedin,register,viewProfile,viewCustomers,updateprofile,changepassword,addlead,addproduct,viewproducts,viewlead,viewEmployees
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from django.urls import path
urlpatterns = [
    url(r'^login/$',login),
    url(r'^auth/$',auth_view),
    url(r'^logout/$',logout),
    url(r'^loggedin/$',loggedin),
    url(r'^invalidlogin/$',invalidlogin),
    url(r'^registration/$',register),
    url(r'^viewprofile/$',viewProfile),
    url(r'^viewcustomers/$',viewCustomers),
    url(r'^updateprofile/$',updateprofile),
    url(r'^updatepassword/$',changepassword),
     url(r'^viewleads/$',viewlead),
    url(r'^addlead/$',addlead),
    url(r'^add_product/$',addproduct),
    url(r'^viewproducts/$',viewproducts),
    url(r'^viewemployees/$',viewEmployees),
]
