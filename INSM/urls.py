

from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [#add_distribution

    path('INSMHome/'                               , INSMHOME                                , name='INSMHome'                       ),
 
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)