from django.urls import path
from . import views
# urls.py
import os,sys
import django
from django.conf import settings
from django.conf.urls.static import static

#


urlpatterns = [   
    #path('', tache.list_files_in_directory, name="list_files_in_directory"),
   # path('', views.requete, name="requete")

    #path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('modif/<str:age>/<str:nsous>/', views.modifier, name='modifier'),
    path('se/', views.segments, name='segments'),
    path('liste_actions/', views.liste_actions, name='liste_actions'),
    
]