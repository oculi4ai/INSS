from django.contrib import admin
from .models import Profile,App,mail,Folder,File


admin.site.register(App)
admin.site.register(Profile)
admin.site.register(mail)
admin.site.register(Folder)
admin.site.register(File)
