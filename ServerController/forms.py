from django.contrib.auth.forms import AuthenticationForm
from django import forms

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username','style':''' color:white;background-color: #0e1621;border: 0px;  padding:5px;  border-radius: 6px;  margin-top: 2px;  margin-bottom: 20px;  width: 250px;  text-align:center;'''}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password','style':''' color:white;background-color: #0e1621;border: 0px;  padding:5px;  border-radius: 6px;  margin-top: 2px;  margin-bottom: 20px;  width: 250px;  text-align:center;'''}))


class select_model_name(forms.Form):
    name = forms.CharField(max_length=100)


class SET_SYNCH_USER_FORM(forms.Form):
    username = forms.CharField(max_length=100)
    