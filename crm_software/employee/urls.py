from employee.views import addtransaction,employeeloggedin,viewtransactions,viewcustomers,viewprofile,updateprofile,changepassword
from django.conf.urls import url
from django.urls import path
urlpatterns = [
    url(r'^addtransaction/$', addtransaction),
    url(r'^emp/$', employeeloggedin),
    url(r'^viewtransactions/$', viewtransactions),
    url(r'^viewempprofile/$', viewprofile),
    url(r'^viewmycustomers/$', viewcustomers),
    url(r'^updateempprofile/$', updateprofile),
    url(r'^updateemppassword/$', changepassword),

]