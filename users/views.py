from django.shortcuts import render, redirect
from .forms import *
import datetime, json
from .models import *
from django.views.generic import DetailView
from django.http import JsonResponse, request

def send_mail(request, user_to=False , subject=False):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':

            try:
            
                user = User.objects.get(username = request.POST['username_to'])
                new_mail= mail.objects.create(
                        username_from   = request.user,
                        username_to     = user,
                        subject         = request.POST['subject'],
                        body            = request.POST['body'],
                        sending_datetime= datetime.datetime.now().isoformat(),
                        received        = 0,
                        readed          = 0,
                    )


                user.profile.new_mail_inbox = json.dumps(json.loads(user.profile.new_mail_inbox) + [new_mail.id ,])
                user.save()
                user.profile.save()
                
                request.user.profile.new_mail_outbox = json.dumps(json.loads(request.user.profile.new_mail_outbox) + [new_mail.id ,])
                request.user.profile.save()


                data = {
                    'form': SendMailForm(),
                    'user_to':user_to,
                    'subject':subject,
                    }

                return redirect('mailView')
                    

            except:
                data = {'form': SendMailForm(), 'message' : 'user not fount'}
                return render(request, 'send_mail.html', data)
                

        else:
            data = {
                    'form': SendMailForm(),
                    'user_to':user_to,
                    'subject':subject,
                    }
            return render(request, 'send_mail.html', data)

def view_mail(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        obj_inbox =  mail.objects.filter(pk__in = json.loads(request.user.profile.new_mail_inbox) ).all()
        obj_outbox =  mail.objects.filter(pk__in = json.loads(request.user.profile.new_mail_outbox)).all()
        obj_edited =  mail.objects.filter(pk__in = json.loads(request.user.profile.mail_edited)).all()
        inbox=[]
        outbox=[]
        edited =[]


        for obj in obj_inbox:
            obj.received=True
            obj.save()
            inbox.append({
                'pk'                : obj.pk , 
                'username_from'     : obj.username_from.username , 
                'subject'           : obj.subject , 
                'body'              : obj.body , 
                'sending_datetime'  : obj.sending_datetime , 
                'received'          : obj.received , 
                'readed'            : obj.readed , 
            })

        for obj in obj_outbox:
            outbox.append({
                'pk'                : obj.pk , 
                'username_to'       : obj.username_to.username , 
                'subject'           : obj.subject , 
                'body'              : obj.body , 
                'sending_datetime'  : obj.sending_datetime , 
                'received'          : obj.received , 
                'readed'            : obj.readed , 
            })
        for obj in obj_edited:
            if request.user == obj.username_from:
                u = obj.username_to.username
            
            elif request.user == obj.username_to:
                u = obj.username_from.username


            edited.append({
                'pk'                : obj.pk , 
                'user'              : u , 
                'subject'           : obj.subject , 
                'body'              : obj.body , 
                'sending_datetime'  : obj.sending_datetime , 
                'received'          : obj.received , 
                'readed'            : obj.readed , 
            })

        mails = {
            'inbox': inbox,
            'outbox': outbox,
            'edited': edited,
        }
        request.user.profile.new_mail=False
        request.user.profile.save()
        request.user.profile.new_mail_inbox     = '[]'
        request.user.profile.new_mail_outbox    = '[]'
        request.user.profile.mail_edited        = '[]'
        request.user.profile.save()
        return JsonResponse(mails)


def addFolder(request , main_folder ):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            MF = Folder.objects.get(pk = main_folder )
            print(request.POST.get('name'))
            if request.POST.get('privet') == 'on':
                privet = True
            else:
                privet = False

            Folder.objects.create( name = request.POST.get('name') , privet = privet , owner = request.user  , MainFolder = MF)
            return redirect('personal_storage' , main_folder)
        else:
            return render(request, 'add_folder.html', {'form' : FolderForm(), 'main_folder' : main_folder})
            

def addFile(request , main_folder ):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            MF = Folder.objects.get(pk = main_folder )
            form = FileForm(request.POST or None, request.FILES)

            if request.POST.get('privet') == 'on':
                privet = True
            else:
                privet = False
            


            File.objects.create( name = request.POST.get('name') , file = form.files['file'] ,  privet = privet , owner = request.user  , MainFolder = MF)
            print('created')
            return redirect('personal_storage' , main_folder)

        else:
            return render(request, 'add_file.html', {'form' : FileForm(), 'main_folder' : main_folder})
            



class ReadMail(DetailView):
   	model 		= mail
   	object_name = 'mail'

   	def get(self,*args, **kwargs):
   	    c_mail = mail.objects.get(pk=self.kwargs['pk']) 
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')

   	    elif self.request.user not in ( c_mail.username_from , c_mail.username_to ):
   	        return redirect('accessDenied')

   	    else:
   	        if c_mail.username_to == self.request.user:
   	            c_mail.readed=True
   	            c_mail.save()

   	        
   	        return super().get(*args, **kwargs)




class FolderView(DetailView):
   	model 		= Folder


   	        
   	def get_context_data(self, **kwargs):
   	    
   	    context = super().get_context_data( **kwargs)
   	    folder=Folder.objects.get(pk=self.kwargs['pk'])

   	    if self.request.user == folder.owner:    
   	        form =FileForm(instance=folder)
   	        context['form'] = form

   	    return context
    
   	def get(self,*args, **kwargs):
   	    folder=Folder.objects.get(pk=self.kwargs['pk'])
   	    
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')

   	    elif (folder.privet) and (self.request.user != folder.owner)  :
   	        return redirect('accessDenied')

   	    else:
   	        return super().get(*args, **kwargs)

   	def post(self, request, *args, **kwargs):
   	    
   	    if 'edit' in request.POST:
   	        folder=Folder.objects.get(pk=self.kwargs['pk'])
   	                                  
            
   	        if request.POST.get('privet') == 'on':
   	            privet = True
   	        else:
   	            privet = False

   	        folder.name   = request.POST.get('name')
   	        folder.privet = privet 
   	        folder.save()
   	        return redirect('folder' , self.kwargs['pk'] )

   	    elif 'delete' in request.POST:
   	        folder=Folder.objects.get(pk=self.kwargs['pk']) 
   	        main_pk = folder.MainFolder.pk
   	        folder.delete()

   	        return redirect('personal_storage', folder = main_pk)



class FileView(DetailView):
   	model 		= File


   	        
   	def get_context_data(self, **kwargs):
   	    
   	    context = super().get_context_data( **kwargs)
   	    file=File.objects.get(pk=self.kwargs['pk'])

   	    if self.request.user == file.owner:    
   	        form =FileForm(instance=file)
   	        context['form'] = form

   	    return context
    
   	def get(self,*args, **kwargs):
   	    file=File.objects.get(pk=self.kwargs['pk'])
   	    
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')

   	    elif (file.privet) and (self.request.user != file.owner)  :
   	        return redirect('accessDenied')

   	    else:
   	        return super().get(*args, **kwargs)

   	def post(self, request, *args, **kwargs):
   	    
   	    if 'edit' in request.POST:

   	        file=File.objects.get(pk=self.kwargs['pk'])
   	                                  
            
   	        if request.POST.get('privet') == 'on':
   	            privet = True
   	        else:
   	            privet = False

   	        file.name   = request.POST.get('name')

   	        if 'file' in request.FILES.keys():
   	            file.file   = request.FILES['file']
            
   	        file.privet = privet
   	        file.save()
   	        return redirect('file' , self.kwargs['pk'] )

   	    elif 'delete' in request.POST:
   	        print('delete')
   	        file=File.objects.get(pk=self.kwargs['pk'])   	        

   	        main_pk = file.MainFolder.pk

   	        file.delete()
   	        return redirect('personal_storage', folder = main_pk)
