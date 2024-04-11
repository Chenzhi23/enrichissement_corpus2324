from django.shortcuts import render
from app01 import models
# Create your views here.

def dynamique_list(request):
    '''dunamique列表'''
    # queryset：[对象，对象，对象]
    queryset = models.EnrichiDynamique.objects.all()

    return render(request, 'dynamique_list.html', {'queryset': queryset})