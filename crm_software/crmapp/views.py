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
# Create your views here.
from customer.models import employee_customer, customer_logins, lead_status
from customer.models import transaction
from django.core.mail import send_mail
def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)

        uid = request.user.id
        user = UserType.objects.get(user_id=uid)
        request.session['user_type'] = user.user_type
        print("sending email")
        # send_mail('Welcome to CRMAPP ', 'test', 'priyalrdesai99@gmail.com', ['priyalrdesai99@gmail.com'],
        #           fail_silently=False)
        if user.user_type == "manager":

            return HttpResponseRedirect('/crmapp/loggedin/')
        elif user.user_type == "employee":

            return HttpResponseRedirect('/employee/emp/')
        else:
            u=customer_logins.objects.get(customer_id=uid)
            c=u.number
            u.number=c+1
            if u.number>5 and u.number<10:
                l=lead_status.objects.get(customer_id=uid)
                l.lead="warm"
                l.save()
            if u.number>10:
                l = lead_status.objects.get(customer_id=uid)
                l.lead = "hot"
                l.save()
            u.save()
            return HttpResponseRedirect('/customer/viewpurchases/')
    else:
        return render_to_response('login.html',{"msg":"Invalid userame or password"})

@login_required(login_url = '/crmapp/login/')
def loggedin(request):
    if request.user.is_authenticated:
        salesData = [0] * 13
        salesCount = [0] * 13
        sales = transaction.objects.all()
        for sal in sales:
            salesData[sal.date.month] = int(salesData[sal.date.month]) + int(sal.product.sell_price)
        # print(sales[len(sales)-1].r_date.month)
        salcount = transaction.objects.raw(
            "SELECT count(id) as count,id,date,product_id FROM `customer_transaction` GROUP by month(date),year(date) ")
        for x in salcount:
            salesCount[x.date.month] = x.count
        data = [299, 3000, 2000, 1000, 1111, 111, 2222, 5499, 2222]
        warm = lead_status.objects.filter(lead="warm")
        hot = lead_status.objects.filter(lead="hot")
        cold = lead_status.objects.filter(lead="cold")
        if len(sales) - 1<0:
            return render(request,'loggedin.html')
        return render(request, 'loggedin.html',
                      {"data": salesCount[1:sales[len(sales) - 1].date.month + 1],

                       "salesData": salesData[1:sales[len(sales) - 1].date.month + 1],"hot":len(hot),"warm":len(warm),"cold":len(cold),"totalleads":len(hot)+len(cold)+len(warm)})
        return render(request,'loggedin.html')
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})


def invalidlogin(request):
    if request.user.is_authenticated:
        return render_to_response('invalidlogin.html')
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request,'login.html', {"msg": "You have logged out"})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

def register (request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user_type = request.POST.get('user_type', '')
            user_name = request.POST.get('username', '')
            mail=request.POST.get('email', '')
            user = User.objects.get(username=user_name)
            if user_type == 'customer':
                c = customer_logins.objects.create(customer_id=user.id,customer_name = user_name,number = 0)
                l = lead_status.objects.create(customer_id=user.id,lead="cold")
                l.save()
                c.save()
                print("sending email")
                send_mail('Welcome to CRMAPP ', 'test','priyalrdesai99@gmail.com', [mail], fail_silently=False)

            u = UserType.objects.get(user_id=user.id)
            u.user_type = user_type
            u.user_name = user_name
            u.save()
            return render_to_response('login.html', {"msg": "Enter your details for logging in"})
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

@login_required(login_url = '/crmapp/login/')
def viewProfile(request):
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
        return render(request,'viewprofile.html',{"user_type":ut})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def viewCustomers(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="manager":
            u=customer_logins.objects.all()
            l=lead_status.objects.all()
            warm=lead_status.objects.filter(lead="warm")
            hot = lead_status.objects.filter(lead="hot")
            cold = lead_status.objects.filter(lead="cold")
            return render(request,'viewcustomers.html',{"users":u,"lead":l,"hot":len(hot),"warm":len(warm),"cold":len(cold)})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def viewEmployees(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="manager":
            u = UserType.objects.filter(user_type="employee")
            c = UserType.objects.filter(user_type="customer")


            if request.method == 'GET':
                request.session["cid"] =request.GET.get('id')
                emp_id = request.GET.get('id')
                if not emp_id:
                    return render(request, 'viewemployees.html', {"emp": u})
                else:
                    cust = transaction.objects.filter(employee_id=emp_id)
                    cid=cust[0].employee_id
                    return render(request, 'viewemployees.html', {"emp": u,"cust":cust,"cid":cid})




            return render(request,'viewemployees.html',{"emp":u})
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
            return render(request,'viewprofile.html')
        else:
            form = PasswordChangeForm(request.user)
            request.session['error_msg']="Enter the old password properly"
            return render(request, 'updatepassword.html',{'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'updatepassword.html', {'form': form})

@login_required(login_url = '/crmapp/login/')
def updateprofile(request):
    if request.user.is_authenticated:
        return render(request, 'updateprofile.html')
    else:
        return render(request, 'login.html', {'msg':"Please login first"})

@login_required(login_url = '/crmapp/login/')
def viewlead(request):
    if request.user.is_authenticated:
        uid = request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type == "manager":
            user1 = User.objects.raw("SELECT id,username FROM `auth_user` where id in(select employee_id from customer_employee_customer)  ")
            ci = employee_customer.objects.all()
            if request.method == 'GET':
                name = request.GET.get('name')
                if not name:
                    return render(request, 'viewleads.html', {'empcust': user1, 'ci': ci})
                else:

                    # Product_details.objects.raw('delete from Product_details where id = ?',( pid,))
                    query = employee_customer.objects.get(customer_name=name)
                    query.delete()
                    ci = employee_customer.objects.all()
                    return render(request, 'viewleads.html', {'empcust': user1, 'ci': ci})

            return render(request, 'viewleads.html',{'empcust':user1,'ci':ci})

    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def addlead(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="manager":
            if request.method == 'POST' and request.POST.get('employee','')!= 'NULL':
                ename=request.POST.get('employee','')
                cname = request.POST.get('customer', '')
                eid = User.objects.get(username=ename).id
                cid = User.objects.get(username=cname).id
                ec = employee_customer(customer_name=cname, customer_id=cid,employee_id=eid)
                ec.save()
                return viewlead(request)

            e=UserType.objects.filter(user_type="employee")
            customer="customer"
            c = User.objects.raw("SELECT id,username FROM `auth_user` where id not in(select customer_id from customer_employee_customer) and id in(select user_id from crmapp_usertype where user_type=\'customer \') ")

            ci=employee_customer.objects.all()
          #  request.session["customers"]=UserType.objects.filter(user_type="customer")
            return render(request,'addlead.html',{'employees':e,'customers':c,'cin':ci})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def addproduct(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="manager":
            if request.method == 'POST':
                name = request.POST.get('name', '')
                costprice = request.POST.get('cprice', '')
                sellprice = request.POST.get('sprice', '')
                description = request.POST.get('description', '')
                p = Product_details(name=name, cost_price=costprice,sell_price=sellprice, description=description)

                # for i in customers:
                # send_mail('Welcome to CRMAPP ', 'test', 'priyalrdesai99@gmail.com', [mail], fail_silently=False)
                p.save()
                # send_mail('Testing mail'+pname, 'This is an auto generated mail product added'+pname, 'adchaudhari70@outlook.com', ['adchaudhari70.ac@gmail.com'],fail_silently=False)
                return viewproducts(request)
            else:
                return render(request,'add_product.html')
        else:
            message = "Login in as manager to access this page."
            return render(request, 'loggedin.html', {'message': message})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

@login_required(login_url = '/crmapp/login/')
def viewproducts(request):
    if request.user.is_authenticated:
        uid=request.user.id
        user = UserType.objects.get(user_id=uid)
        if user.user_type=="employee" or user.user_type=="manager":
            product = Product_details.objects.all()
            if user.user_type == "manager":
                if request.method == 'GET':
                    pid = request.GET.get('id')
                    if not pid:

                        return render(request, 'viewproducts.html', {"products": product})
                    else:

                        #Product_details.objects.raw('delete from Product_details where id = ?',( pid,))
                        query = Product_details.objects.get(id=pid)
                        query.delete()
                        product = Product_details.objects.all()
                        return render(request, 'viewproducts.html',{"products": product})
                else:
                    return render(request, 'viewproducts.html', {"products": product})
            else:
                return render(request, 'viewproducts.html', {"products": product})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

