from django.shortcuts import render,redirect
import sys
import os
from django.contrib.auth import authenticate, login
from .forms import  *
from django import forms
from users.models import *
from INSServer import settings# import SYNCH_USER,SYNCH_TIMER
from django.contrib.auth.models import User
import time, threading
from django.http import FileResponse, HttpResponse, JsonResponse
import mimetypes
import os, configparser, sys
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import DetailView  ,ListView
from django.core.management import execute_from_command_line

# Create your views here.
def home(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		return render(request , 'index.html' )


def profile(request):
    if not request.user.is_authenticated:
    	return redirect('login')
    else:
    	return render(request , 'profile.html' )


def Settings(request):
    if not request.user.is_authenticated:
    	return redirect('login')
    elif request.user.profile.user_app.name == 'INSM':

    	config = configparser.ConfigParser()
    	config.read('settings.ini')

    	if request.method == 'POST':
    		if 'time_zone' in request.POST:
    			print(request.POST)
    			try:
    				config['INFO']['TZ_GMT'] = str(int(request.POST['value']))
    				config.write(open('settings.ini','w'))
    				settings.TIME_ZONE = 'Etc/GMT+'+ config['INFO']['TZ_GMT']

					# this to codes to rewrite file to make the server reload
    				old_file = open( os.path.join('ServerController','admin.py'),'r').read()
    				open( os.path.join('ServerController','admin.py'),'w').write(old_file)

    			except:
    				pass

    			data = {
				'TIME_ZONE_GMT' :  config['INFO']['TZ_GMT'],
				}
    			return render(request , 'settings.html', data )
				
    	else:
    		data = {
				'TIME_ZONE_GMT' :  config['INFO']['TZ_GMT'],
			}
    		return render(request , 'settings.html', data )

    else:
    	return redirect('accessDenied')


	

def mail_home(request):
    
    if not request.user.is_authenticated:
    	return redirect('login')
    else:
    	new_mails_ids = set.union( set(Mail_CC_Receiver.objects.filter(user = request.user,readed=False ).values_list('user', flat=True)) , set(Mail_BCC_Receiver.objects.filter(user = request.user,readed=False ).values_list('user', flat=True)))
    	print(new_mails_ids)
    	new_mails = mail.objects.filter(pk__in = new_mails_ids)
    	if len(new_mails)>3 :
    		new_mails_objects = new_mails[:3]
    	else:
    		new_mails_objects = new_mails


    	
    	mails = mail.objects.filter(username_from = request.user)
    	contacts_ids = set.union(
			set(Mail_CC_Receiver.objects.filter( mail__in = mails).values_list('user', flat=True)),
			set(Mail_BCC_Receiver.objects.filter( mail__in = mails).values_list('user', flat=True))
		)
    	contacts = User.objects.filter(pk__in = contacts_ids)

		
    	

    	return render(request , 'mail-home.html', { 'new_messages_count': 3 ,'new_messages': new_mails_objects, 'contacts':contacts } )



class CCInboxMailView(ListView):
	model 				= Mail_CC_Receiver
	context_object_name = 'mail'
	template_name 		= 'cc-inbox-mail.html'
	paginate_by			= 12
	ordering 			= ['-created_date']

	def get_queryset(self):
		queryset = super().get_queryset()
		return  queryset.filter(user = self.request.user)



class BCCInboxMailView(ListView):
	model 				= Mail_BCC_Receiver
	context_object_name = 'mail'
	template_name 		= 'bcc-inbox-mail.html'
	paginate_by			= 12
	ordering 			= ['-created_date']

	def get_queryset(self):
		queryset = super().get_queryset()
		return  queryset.filter(user = self.request.user)



class OutboxMailView(ListView):
	model 		= mail
	context_object_name = 'mail'
	template_name = 'outbox-mail.html'
	paginate_by=12
	ordering = ['-sending_datetime']

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(username_from=self.request.user)



def accessDenied(request):
    if not request.user.is_authenticated:
    	return redirect('login')
    else:
    	return render(request , 'accessDenied.html' )


def SYNCH_USER_TIMER(user):
	settings.SYNCH_USER = user

	while True:
		time.sleep(1)
		settings.SYNCH_TIMER=settings.SYNCH_TIMER-1
		
		if settings.SYNCH_TIMER <=0:
			break
	settings.SYNCH_USER = None



def SET_SYNCH_USER(request):
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		if request.method == 'POST':
			username = SET_SYNCH_USER_FORM(request.POST).data['username']
			print(username,settings.SYNCH_USER == None)
			red = render(request, 'SET_SYNCH_USER.html', {'form': SET_SYNCH_USER_FORM()})


			if settings.SYNCH_USER == None:
				try:
					user = User.objects.get(username=username)
					settings.SYNCH_TIMER=40
					threading.Thread(target=SYNCH_USER_TIMER, args=(user,)).start()
					red.set_cookie(key ='status', value = 1)

				except:
					red.set_cookie(key ='status', value = 0)
			
			else:
				try:
					if settings.SYNCH_USER == User.objects.get(username=username):
						settings.SYNCH_TIMER=40
						red.set_cookie(key ='status', value = 1)
				except:

					red.set_cookie(key ='status', value = 0)
			
			return red
		else:
			return render(request, 'SET_SYNCH_USER.html', {'form': SET_SYNCH_USER_FORM()})


def view_login(request):
	
	if request.method == 'POST':
		form = UserLoginForm( data=request.POST )
		user = form.get_user()


		if form.is_valid(): 
			user = authenticate( username=form.data['username'], password=form.data['password'])
			print(user)
			if user is not None:
				login(request= request,user=user)
			try:
				
				if user.profile.database_code == None or user.profile.database_code == form.data['database_code']:
					if user.profile.database_code == None:
						profile=Profile.objects.get(user=user)
						print(profile.database_code)
						profile.database_code = form.data['database_code']
						profile.save()
					
					if user.profile.user_app.name == form.data['app']:
						return redirect('home')
					else:
						red = render(request, 'login.html' , {'form': form})
						re_app= form.data['app']
						red.set_cookie(key ='message', value = f'You are trying to login with {user.profile.user_app.name} account by { re_app } app')
						return red

				
				else:
					red = render(request, 'login.html' , {'form': form})
					red.set_cookie(key ='message', value = '''You can not connect to INSServer with this file <br/>make sure database code set correctly on server databases''')
					return red
			except:
					return redirect(user.profile.user_app.name+'Home')

		else:
			
			red = render(request, 'login.html' , {'form': form})
			red.set_cookie(key ='message', value = 'Access denied')
			return red


	if request.method == 'GET':
		form = UserLoginForm()

		return render(request, 'login.html' , {'form': form})



def personal_storage(request, folder):

	current_item = Folder.objects.get(pk = folder) 
	if current_item.owner == request.user or not current_item.privet:

		folders = Folder.objects.filter(MainFolder = folder)
		files 	= File.objects.filter(MainFolder = folder)

		if len(folders)==0 and len(files)==0 : 
			empty = True

		else:
			empty = False

		return render(request, 'personal_storage.html' , {'folders' : folders , 'files':files , 'current_item' : current_item , 'empty' : empty  } )
	
	else:
		return redirect('accessDenied')



def personal_storage_API(request, folder):

	current_item = Folder.objects.get(pk = folder) 
	if current_item.owner == request.user or not current_item.privet:

		folders = Folder.objects.filter(MainFolder = folder)
		files 	= File.objects.filter(MainFolder = folder)

		if len(folders)==0 and len(files)==0 : 
			empty = True

		else:
			empty = False

		API_folders = []
		API_files = []
		for folder in folders:
			API_folders.append(
				{
					'name'     	:folder.name,
					'pk'     	:folder.pk,
					'privet'    :folder.privet,
					'MainFolder':folder.MainFolder.pk,
				}
			)
		
		for file in files:
			API_files.append(
				{
					'name' : file.name,
					'pk' : file.pk,
					'file' : file.file.url,
					'privet' : file.privet,
					'MainFolder' : file.MainFolder.pk,
				}
			)

		out_data = {
				'name': current_item.name ,
				'folders' : API_folders , 
				'files':API_files }
			
		
		if current_item.MainFolder:
			

			if current_item.MainFolder.MainFolder:
				

				if current_item.MainFolder.MainFolder.MainFolder:
					out_data['p1_folder'] = current_item.MainFolder.MainFolder.MainFolder.pk
					out_data['p1_folder_name'] = current_item.MainFolder.MainFolder.MainFolder.name

					out_data['p2_folder'] = current_item.MainFolder.MainFolder.pk
					out_data['p2_folder_name'] = current_item.MainFolder.MainFolder.name

					out_data['p3_folder'] = current_item.MainFolder.pk
					out_data['p3_folder_name'] = current_item.MainFolder.name

				else:
					out_data['p1_folder'] = current_item.MainFolder.MainFolder.pk
					out_data['p1_folder_name'] = current_item.MainFolder.MainFolder.name

					out_data['p2_folder'] = current_item.MainFolder.pk
					out_data['p2_folder_name'] = current_item.MainFolder.name


			else:
				out_data['p1_folder'] = current_item.MainFolder.pk
				out_data['p1_folder_name'] = current_item.MainFolder.name


		print(out_data)


		return JsonResponse(out_data, safe=False)
	
	else:
		return redirect('accessDenied')



def main_personal_storage_API(request):
	folder = request.user.profile.storage_file_pk 
	current_item = Folder.objects.get(pk = folder) 
	if current_item.owner == request.user or not current_item.privet:

		folders = Folder.objects.filter(MainFolder = folder)
		files 	= File.objects.filter(MainFolder = folder)

		if len(folders)==0 and len(files)==0 : 
			empty = True

		else:
			empty = False

		API_folders = []
		API_files = []
		for folder in folders:
			API_folders.append(
				{
					'name'     	:folder.name,
					'pk'     	:folder.pk,
					'privet'    :folder.privet,
					'MainFolder':folder.MainFolder.pk,
				}
			)
		
		for file in files:
			API_files.append(
				{
					'name' : file.name,
					'pk' : file.pk,
					'file' : file.file.url,
					'privet' : file.privet,
					'MainFolder' : file.MainFolder.pk,
				}
			)


		return JsonResponse({'name': current_item.name ,'folders' : API_folders , 'files':API_files }, safe=False)
	
	else:
		return redirect('accessDenied')

def download_file(request, file_pk):
	path = File.objects.get(pk = file_pk).file.path 
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response


