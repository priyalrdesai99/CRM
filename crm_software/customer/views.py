from django.shortcuts import render

# Create your views here.
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth,messages
from django.template.context_processors import csrf
from crmapp.models import UserType, Product_details
from django.contrib.auth.models import User
from django.contrib.auth.forms import  PasswordChangeForm
# Create your views here.
from customer.models import employee_customer, customer_logins
from customer.models import transaction



@login_required(login_url='/crmapp/login/')
def viewtransactions(request):
    uid = request.user.id
    name = User.objects.get(id=uid).username
    t = transaction.objects.filter(customer_name=name)
    return render(request, 'viewpurchases.html', {'trans': t})

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
            return render(request,'viewcusprofile.html')
        else:
            form = PasswordChangeForm(request.user)
            request.session['error_msg']="Enter the old password properly"
            return render(request, 'updatecuspassword.html',{'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'updatecuspassword.html', {'form': form})

@login_required(login_url = '/crmapp/login/')
def updateprofile(request):
    if request.user.is_authenticated:
        return render(request, 'updatecusprofile.html')
    else:
        return render(request, 'login.html', {'msg':"Please login first"})

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
        return render(request,'viewcusprofile.html',{"user_type":ut})
    else:
        return render_to_response('login.html', {"msg": "Invalid access first login"})

