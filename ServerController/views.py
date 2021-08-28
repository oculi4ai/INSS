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
import os
from django.conf import settings
from django.http import HttpResponse, Http404


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


def mailView(request):
    if not request.user.is_authenticated:
    	return redirect('login')
    else:
    	return render(request , 'mail.html' )

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
					'privet'    :folder.privet,
					'MainFolder':folder.MainFolder.pk,
				}
			)
		
		for file in files:
			API_files.append(
				{
					'name' : file.name,
					'file' : file.file.url,
					'privet' : file.privet,
					'MainFolder' : file.MainFolder.pk,
				}
			)

		print(API_folders)
		return JsonResponse({'folders' : API_folders , 'files':API_files }, safe=False)
	
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
					'file' : file.file.url,
					'privet' : file.privet,
					'MainFolder' : file.MainFolder.pk,
				}
			)

		print(API_folders)
		return JsonResponse({'folders' : API_folders , 'files':API_files }, safe=False)
	
	else:
		return redirect('accessDenied')

def download_file(request, file_pk):
	path = File.objects.get(pk = file_pk).file.path 
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response


