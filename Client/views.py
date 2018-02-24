# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.forms import formset_factory
from .forms import AddExpenseForm, ProductForm, AddCurrencyCodeForm
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import ExpensesTracker, ExpenseProduct, CurrencyCode
import code
from django.db import transaction
from django.contrib.auth.models import User

# Create your views here.
@transaction.atomic
def addCurrencyCode(request):
    if request.method == 'GET':
        form = AddCurrencyCodeForm()
        return render(request,'addcurrencycode.html',{'form':form})
    elif request.method == 'POST':
        form = AddCurrencyCodeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['currencycode']
            currency = CurrencyCode.objects.create(currency_name=name,currency_code=code)
            currency.save()
            return HttpResponseRedirect('/addcurrencycode/')
        else:
            return render(request,'addcurrencycode.html',{'form':form})
    else:
        return HttpResponseRedirect('/homepage/')

@transaction.atomic
def addExpense(request):
    productformset = formset_factory(ProductForm)
    if request.method == 'GET':
        form = AddExpenseForm()
        return render(request, 'addexpense.html',{'form':form,'productformset':productformset})
    elif request.method == 'POST':
        form = AddExpenseForm(request.POST)
        productforms = productformset(request.POST)
        if form.is_valid() and productforms.is_valid():
            expensedon = form.cleaned_data['expensedon']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['price']
            user = User.objects.get(id=request.session['userid'])
            expense = ExpensesTracker.objects.create(expensed_on=expensedon,title=title,description=description,amount=amount,client=user)
            for frm in productforms:
                product_name = frm.cleaned_data['productname']
                product_type = frm.cleaned_data['producttype']
                quantity = frm.cleaned_data['quantity']
                cost = frm.cleaned_data['price']
                expenseproduct = ExpenseProduct.objects.create(product_name=product_name,product_type=product_type,quantity=quantity,cost=cost,expensetracker=expense)
                expenseproduct.save()
            return HttpResponseRedirect('/viewexpense/%s/' %expense.id)
        else:
            return render(request, 'addexpense.html',{'form':form,'productformset':productformset})
    else:
        return HttpResponseRedirect('/listexpenses/')

def viewExpense(request,expid):
    if request.method == 'GET':
        try:
            expense = ExpensesTracker.objects.get(id=expid,client__id=request.session['userid'])
            expproducts = ExpenseProduct.objects.filter(expensetracker=expense)
            return render(request,'viewexpense.html',{'expense':expense,'expproducts':expproducts})
        except ExpensesTracker.DoesNotExist:
            return HttpResponseRedirect('/listexpense/')
    else:
        return HttpResponseRedirect('/listexpense/')
    
    
def listexpenses(request):
    if request.method == 'GET':
        expenses = ExpensesTracker.objects.filter(client__id=request.session['userid'])
        return render(request,'listexpense.html',{'expenses':expenses})
    else:
        return HttpResponseRedirect('/addexpense/')
            