from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class App(models.Model):
    name                    =  models.CharField( max_length=200)
    icon_path               =  models.CharField( max_length=200)
    home_path               =  models.CharField( max_length=200)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user                    =  models.OneToOneField(User, null=True, blank=True ,on_delete=models.CASCADE)
    database_code	        =  models.CharField( max_length=200, default=None,null=True, blank=True )
    user_app                =  models.ForeignKey(App, null=True, blank=True ,on_delete=models.CASCADE)
    new_mail_inbox          =  models.CharField( max_length=20000, default='[]',null=True, blank=True )
    new_mail_outbox         =  models.CharField( max_length=20000, default='[]',null=True, blank=True )
    mail_edited             =  models.CharField( max_length=20000, default='[]',null=True, blank=True )#when receved or readed
    storage_file_pk         =  models.IntegerField(default= 0)
    
    
    
    def __str__(self):
        return self.user.username




class mail(models.Model):
    username_from   =  models.ForeignKey(User, null=True, blank=True ,on_delete=models.CASCADE,  related_name='username_from')
    username_to     =  models.ForeignKey(User, null=True, blank=True ,on_delete=models.CASCADE,  related_name='username_to')
    subject         =  models.CharField( max_length=200, default=None,null=True, blank=True )
    body            =  models.TextField()
    sending_datetime=  models.DateTimeField()
    received        =  models.BooleanField()
    readed          =  models.BooleanField()



class Folder(models.Model):
    name            = models.CharField( max_length=200, default='New Folder')
    owner           = models.ForeignKey( User , null=True, blank=True ,on_delete=models.CASCADE)    
    privet          = models.BooleanField(default=True)
    MainFolder      = models.ForeignKey('self', null=True, blank=True ,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name

class File(models.Model):
    name            = models.CharField( max_length=200, default='New file')
    file            = models.FileField(upload_to='users_files')
    owner           = models.ForeignKey( User , null=True, blank=True ,on_delete=models.CASCADE)    
    privet          = models.BooleanField(default=True)
    MainFolder      = models.ForeignKey(Folder, null=True, blank=True ,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name