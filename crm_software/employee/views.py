from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth,messages
from django.template.context_processors import csrf
from crmapp.forms import RegistrationForm
from crmapp.models import UserType, Product_details
from django.contrib.auth.models import User
from django.contrib.auth.forms import  PasswordChangeForm
from crmapp.models import Product_details
from customer.models import employee_customer, transaction


@login_required(login_url='/crmapp/login/')
def addtransaction(request):
    if request.user.is_authenticated:
        uid = request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type == "employee":
            if request.method == 'POST':
                cname = request.POST.get('cname', '')
                amount = request.POST.get('amount', '')
                pname=request.POST.get('pname', '')
                pid=Product_details.objects.get(name=pname).id
                ec = transaction(customer_name=cname, amount=amount , employee_id = uid , product_id=pid)
                ec.save()
                return viewtransactions(request)

            else:
                c = User.objects.raw(
                     "SELECT id,customer_name FROM `customer_employee_customer` where employee_id="+str(uid))
                #cust=employee_customer.objects.filter(employee_id=uid)
                products=Product_details.objects.all()
                return render(request, 'addtransaction.html', {'products': products, 'customers': c})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url='/crmapp/login/')
def viewtransactions(request):
    uid = request.user.id
    t = transaction.objects.filter(employee_id=uid)
    return render(request, 'viewtransactions.html', {'transactions': t})

@login_required(login_url='/crmapp/login/')
def employeeloggedin(request):
    t = []
    l1 = []
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cdate = datetime.date(datetime.now())
    str2 = str(cdate)
    eid =request.user.id
    flag = transaction.objects.filter(employee_id=eid).exists()
    if flag:
        # t=employee_customer.objects.filter(e_id=eid)
        t = transaction.objects.raw(
            "SELECT COUNT(id) as c,id,date FROM `customer_transaction` GROUP by month(date),year(date),employee_id HAVING employee_id=" + str(eid))
        str1 = str(t[0].date)
        s = int(str1[5:7])
        j = s - 1
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in t:
            str1 = i.date
            str1 = str(str1)
            if str1[:4] == str2[:4]:
                data[j] = i.c
                j = j + 1
    # print(data)
    arg = {'data': data, 'list': l1}
    return render(request,'emp.html', arg)


@login_required(login_url='/crmapp/login/')
def viewcustomers(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="employee":
            cust = User.objects.raw("SELECT id,username FROM `auth_user` where id in (select customer_id from customer_employee_customer where employee_id =\'"+str(uid)+'\''+")")
            return render(request,'viewmycustomers.html',{"users":cust})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url='/crmapp/login/')
def viewprofile(request):
    if request.user.is_authenticated:
        uid = request.user.id
        user = UserType.objects.get(user_id=uid)
        ut=user.user_type
        if request.POST:
            uid = request.user.id
            user = User.objects.get(id=uid)
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
        return render(request,'viewempprofile.html',{"user_type":ut})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user,data= request.POST)
        if form.is_valid():
            form.save()
            if request.session.has_key('error_msg'):
                del request.session['error_msg']
           # update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your information was successfully updated!')
            return render(request,'viewempprofile.html')
        else:
            form = PasswordChangeForm(request.user)
            request.session['error_msg']="Enter the old password properly"
            return render(request, 'updateemppassword.html',{'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'updateemppassword.html', {'form': form})

@login_required(login_url = '/crmapp/login/')
def updateprofile(request):
    if request.user.is_authenticated:
        return render(request, 'updateempprofile.html')
    else:
        return render(request, 'login.html', {'msg':"Please login first"})
