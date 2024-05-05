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
        query_dict['nature__contains'] = nature
    if accompli:
        query_dict['accompli__contains'] = accompli
    if proces:
        query_dict['proces__contains'] = proces
    if temps:
        query_dict['temps__contains'] = temps

    queryset = models.EnrichiDynamique.objects.filter(**query_dict)
    return render(request, 'dynamique_list.html', {'queryset': queryset})

def act_list(request):
    '''act列表'''
    query_dict = {}

    act_type = request.GET.get('act_type')

    if act_type:
        query_dict['act_type__contains'] = act_type

    queryset = models.EnrichiAct.objects.filter(**query_dict)

    return render(request, 'act_list.html', {'queryset': queryset})

def nouvelle_list(request):
    query_dict = {}

    cause = request.GET.get('cause')
    res = request.GET.get('res')
    obj = request.GET.get('obj')

    if cause:
        query_dict['cause__contains'] = cause
    if res:
        query_dict['res__contains'] = res
    if obj:
        query_dict['obj__contains'] = obj

    queryset = models.EnrichiNouvelle.objects.filter(**query_dict)
    return render(request, 'nouvelle_list.html', {'queryset': queryset})


def doc_list(request):
    queryset = models.EnrichiDoc.objects.all()
    return render(request, 'doc_list.html', {'queryset': queryset})

def lieu_list(request):
    query_dict = {}

    type = request.GET.get('type')

    if type:
        query_dict['type__contains'] = type

    queryset = models.EnrichiLieu.objects.filter(**query_dict)
    return render(request, 'lieu_list.html', {'queryset': queryset})


def perc_list(request):
    querydict = {}

    perc_type = request.GET.get('perc_type')
    pol = request.GET.get('pol')

    if perc_type:
        querydict['perc_type__contains'] = perc_type
    if pol:
        querydict['pol__contains'] = pol

    queryset = models.EnrichiPerception.objects.filter(**querydict)
    return render(request, 'perc_list.html', {'queryset': queryset})


def temps_list(request):
    querydict = {}

    axe_temps = request.GET.get('axe_temps')
    absolu = request.GET.get('absolu')
    type = request.GET.get('type')

    if axe_temps:
        querydict['axe_temps__contains'] = axe_temps
    if absolu:
        querydict['absolu__contains'] = absolu
    if type:
        querydict['type__contains'] = type

    queryset = models.EnrichiTemps.objects.filter(**querydict)
    return render(request, 'temps_list.html', {'queryset': queryset})


def simple_list(request):
    queryset = models.Simple.objects.all()
    return render(request, 'simple_list.html', {'queryset': queryset})