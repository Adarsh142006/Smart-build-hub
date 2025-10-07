from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from homeownerapp.models import *
from contractorapp.models import*
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    contex = {
        'adminid':adminid,
        'th':userInfo.objects.filter(login__usertype="homeowner").count(),
        'tc':userInfo.objects.filter(login__usertype="contractor").count(),
        'tp':Project.objects.all().count(),
        'trp':Project.objects.filter(status="under_construction").count(),
        'tcp':Project.objects.filter(status="completed").count(),
        'enqs':Enquiry.objects.all().count(),
    }
    return render(request,'admindash.html',contex)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"You are logged out")
        return redirect('adminlogin')
    else:
        return redirect('index')
@cache_control(no_cache=True,must_revalidate=True,no_store=True) 
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    enqs = Enquiry.objects.all()
    return render(request,'viewenq.html',{'enqs':enqs,'adminid':adminid})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enq = Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Enquiry deleted successfully")
    return redirect('viewenq')
    # return render(request,'admindash.html')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def changepass(request):
     if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
     adminid = request.session.get('adminid')
     if request.method == 'POST':
         oldpwd = request.POST.get('oldpwd')
         newpwd = request.POST.get('newpwd')
         confirmpwd = request.POST.get('confirmpwd')
         try:
             admin = LoginInfo.objects.get(username=adminid)
             if admin.password != oldpwd:
                 messages.error(request,"Old password is Inncorrect")
                 return redirect('changepass')
             elif newpwd != confirmpwd:
                   messages.error(request,"New  password and confirm password  is not same")
                   return redirect('changepass')
             elif admin.password == newpwd:
                   messages.error(request,"New  password smae as old password")
                   return redirect('changepass')
             else:
                 admin.password = newpwd
                 admin.save()
                 messages.success(request,"password change successfully")
                 return redirect('admindash')
         except LoginInfo.DoesNotExist:
             messages.error(request,"Something went wrong!")
             return redirect('adminlogin')   
     return render(request,'changepass.html',{'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def managecontractors(request):
    if not 'adminid' in request.session:  
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    contractor = userInfo.objects.filter(login__usertype = 'contractor')
    return render(request,'managecontractors.html',{'adminid':adminid,'contractor':contractor})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    homeowner = userInfo.objects.filter(login__usertype = 'homeowner')
    return render(request,'managehomeowners.html',{'adminid':adminid,'homeowner':homeowner})
