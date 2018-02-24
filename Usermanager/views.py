# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import AddUserForm, LoginForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

# Create your views here.
@transaction.atomic
def addUser(request):
    if request.method == 'GET':
        form = AddUserForm()
        return render(request,'adduser.html',{'form':form})
    elif request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            usr = User.objects.create(username=username,first_name=fname,last_name=lname,email=email)
            usr.set_password(password)
            usr.save()
            return HttpResponseRedirect('/viewuser/?usrid=%s' %usr.id)
        else:
            return render(request,'adduser.html',{'form':form})
    else:
        return HttpResponseRedirect('/homepage/')

def viewUser(request):
    if request.method == 'GET':
        if request.GET.__contains__('usrid'):
            try:
                user = User.objects.get(id=request.GET['usrid'])
                return render(request,'viewuser.html',{'user':user})
            except User.DoesNotExist:
                return HttpResponseRedirect('/listusers/')
        else:
            return HttpResponseRedirect('/listusers/')
    else:
        return HttpResponseRedirect('/homepage/')
    
def listUsers(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request,'listusers.html',{'users':users})
    else:
        return HttpResponseRedirect('/homepage/')
    
def userlogin(request):
    print 'inside method'
    """ User Login  """
    if request.method == 'GET':    
        if request.user.is_authenticated():
            return HttpResponseRedirect('/homepage/')
        else:
            form = LoginForm()
            return render(request,'login.html',{'form':form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print 'inside form post'
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            try:
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    usr = User.objects.get(id=user.id)
                    print usr
                    request.session['userid'] = user.id
                    print request.session['userid']
                    login (request, user)
           
                    return HttpResponseRedirect('/homepage/')
                else:
                    if not user:
                        form._errors['username'] = form.error_class([u''])
                        form._errors['password'] = form.error_class([u'Invalid Username & Password'])
                        return render(request,'login.html',{'form':form})
            except User.DoesNotExist:
                return HttpResponseRedirect('/login/')
        else:
            return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
def dologout (request):
  logout (request)
  return HttpResponseRedirect ('/login/')
  
 
def homepage(request):
    if request.method == 'GET':
        print request.session['userid']
        user = User.objects.get(id=request.session['userid'])
        print user
        return render(request, 'homepage.html',{'user':user})