from django.urls import path
from .views.peca import PecaList

urlpatterns = [path('peca/list/', PecaList, name='pecalist')]
