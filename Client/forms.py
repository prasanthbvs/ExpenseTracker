from django import forms

class AddCurrencyCodeForm(forms.Form):
    name = forms.CharField(max_length=12)
    currencycode = forms.CharField(max_length=12)

class AddExpenseForm(forms.Form):
    expensedon = forms.DateTimeField()
    price = forms.FloatField()
    title = forms.CharField(max_length=256,widget=forms.Textarea(attrs={'rows':'4','cols':'150'}))
    description = forms.CharField(max_length=1024,widget=forms.Textarea(attrs={'rows':'4','cols':'150'}))
    
class ProductForm(forms.Form):
    productname = forms.CharField(max_length=128)
    producttype = forms.CharField(max_length=64)
    quantity = forms.IntegerField()
    price = forms.FloatField()
    