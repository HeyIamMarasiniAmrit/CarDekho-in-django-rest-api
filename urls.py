
from django.urls import path, include
from . import views

urlpatterns = [

    path('pollslist/',views.listpolls,name='listpolls'),
]
