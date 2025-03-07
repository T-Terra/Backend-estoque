from django.urls import path
from .views.peca import PecaAdd

urlpatterns = [path('peca/add/', PecaAdd, name='addpeca')]
