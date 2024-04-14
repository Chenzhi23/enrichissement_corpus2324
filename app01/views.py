from django.shortcuts import render
from app01 import models
# Create your views here.
def index(request):
    return render(request, 'index.html')


def dynamique_list(request):
    '''dunamique列表'''
    # queryset：[对象，对象，对象]
    query_dict = {}

    accompli = request.GET.get('accompli')
    nature = request.GET.get('nature')
    proces = request.GET.get('proces')
    temps = request.GET.get('temps')

    if nature:
        query_dict['nature'] = nature
    if accompli:
        query_dict['accompli'] = accompli
    if proces:
        query_dict['proces'] = proces
    if temps:
        query_dict['temps'] = temps

    queryset = models.EnrichiDynamique.objects.filter(**query_dict)
    return render(request, 'dynamique_list.html', {'queryset': queryset})
