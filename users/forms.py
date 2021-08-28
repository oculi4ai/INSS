from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import mail,Folder,File


class SendMailForm(forms.ModelForm):
    username_to = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username','style':''' color:white;background-color: #0e1621;border: 0px;  padding:5px;  border-radius: 6px; width: 65%; text-align: justify;'''}))
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Subject','style':'''color:white;background-color: #0e1621;border: 0px;  padding:5px;  border-radius: 6px; width: 65%; text-align: justify;'''}))
    body = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Compose mail...','style':''' color:white;background-color: #0e1621;border: 0px;  padding:5px;  border-radius: 6px; width: 100%; text-align: justify;'''}))

    class Meta:
        model=mail
        fields=('username_from','username_to','subject','body','sending_datetime','received','readed')


class MailRecevedForm(forms.Form):
    pks = forms.CharField(max_length=10000)



class FolderForm(forms.ModelForm):
    privet = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxInput()
    )
    class Meta:
        model=Folder
        fields=('name','privet')



class FileForm(forms.ModelForm):
    privet = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxInput()
    )
    class Meta:
        model=File
        fields=('name', 'file' ,'privet')