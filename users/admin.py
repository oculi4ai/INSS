from django.contrib import admin
from .models import *


admin.site.register(App)
admin.site.register(Profile)
admin.site.register(mail)
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Mail_CC_Receiver)
admin.site.register(Mail_BCC_Receiver)



