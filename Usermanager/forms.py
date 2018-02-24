from django import forms

class AddUserForm(forms.Form):
    username = forms.CharField(label="User Name")
    password = forms.CharField(label="Password")
    email = forms.EmailField(label ="E-Mail Address",max_length=128,required=False)
    fname = forms.CharField(label="FirstName",max_length=122,required=True)
    lname = forms.CharField(label="LastName",max_length=122,required=False)
    
class LoginForm(forms.Form):
    username = forms.CharField(label="User Name",widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))