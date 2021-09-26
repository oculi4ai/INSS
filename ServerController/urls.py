
from .views import *
from users.views import *
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', home,name='home'),
    path('profile/', profile,name='profile'),
    path('cc-inbox/', CCInboxMailView.as_view(),name='CCInboxMailView'),
    path('bcc-inbox/', BCCInboxMailView.as_view(),name='BCCInboxMailView'),
    path('outbox/', OutboxMailView.as_view(),name='OutboxMailView'),
    path('login/',  view_login, name='login' ),
    path('SET_SYNCH_USER/',  SET_SYNCH_USER, name='SET_SYNCH_USER' ),
    path('addFolder/?P<int:main_folder>/',  addFolder, name='addFolder' ),#main_personal_storage_API
    path('personal_storage/?P<int:folder>/',  personal_storage, name='personal_storage' ),
    path('main_personal_storage_API/',  main_personal_storage_API, name='main_personal_storage_API' ),
    path('personal_storage_API/<int:folder>/',  personal_storage_API, name='personal_storage_API' ),
    path('addFile/?P<int:main_folder>/',  addFile, name='addFile' ),
    path('replymail/?P<str:user_to>/?P<str:subject>/',  send_mail, name='replymail' ),
    path('sendmail/',  send_mail, name='sendmail' ),
    path('view_mail/',  view_mail, name='view_mail' ),
    path('mail-home/',  mail_home, name='mail_home' ),
    path('AccessDenied/',  accessDenied, name='accessDenied' ),
    path('mail/<int:pk>/', ReadMail.as_view(), name='readmail' ),
    path('file/<int:pk>/', FileView.as_view(), name='file' ),
    path('folder/<int:pk>/', FolderView.as_view(), name='folder' ),
    path('download/<int:file_pk>/', download_file , name='download_file' ),#
    path('settings/', Settings , name='settings' ),
    


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)