from django.db import models

# Create your models here.
class Simple(models.Model):
    '''未enrichi的文件'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom_fichier')
    num_phrase = models.BigIntegerField(primary_key=False,verbose_name='num_phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    lieu_objet = models.TextField(verbose_name='lieu_objet')
    lieu_loc = models.TextField(verbose_name='lieu_loc')
    temps = models.TextField(verbose_name='temps')
    acteurs = models.TextField(verbose_name='acteurs')
    perc = models.TextField(verbose_name='perc')
    doc = models.TextField(verbose_name='doc')


class EnrichiDynamique(models.Model):
    '''<dyn></dyn>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(primary_key=False,verbose_name='numéro de la phrase')
    segment_annote = models.TextField(verbose_name='segment annoté')
    accompli = models.CharField(max_length=32, verbose_name='accompli')
    nature = models.CharField(max_length=32, verbose_name='nature')
    proces = models.CharField(max_length=32, verbose_name='proces')
    temps = models.CharField(max_length=32, verbose_name='temps')


class EnrichiTemps(models.Model):
    '''<tps></tps>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    segment_annote = models.TextField(verbose_name='segment annoté du temps')
    axe_temps = models.CharField(max_length=16, verbose_name='attribut temps')
    absolu = models.CharField(max_length=16, verbose_name='attribut absolu')
    type = models.CharField(max_length=16, verbose_name='attribut type')


class EnrichiLieu(models.Model):
    '''<lieu></lieu>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    segment_annote = models.TextField(verbose_name='segment annoté du lieu')
    type = models.CharField(max_length=16, verbose_name='attribut type de lieu')


class EnrichiPerception(models.Model):
    '''<perc></perc>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    segment_annote = models.TextField(verbose_name='segment annoté de la perception')
    perc_type = models.CharField(max_length=16, verbose_name='attribut du type de la perception')
    pol = models.CharField(max_length=16, verbose_name='attribut pol')


class EnrichiDoc(models.Model):
    '''<doc></doc>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    segment_annote = models.TextField(verbose_name='segment annoté de la doc')


class EnrichiAct(models.Model):
    '''<act></act>'''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    segment_annote = models.TextField(verbose_name='segment annoté act')
    act_type = models.CharField(max_length=16, verbose_name='attribut du type des acts')


class EnrichiNouvelle(models.Model):
    '''
    3 choix de balises dans un tableau nouvelle :
    <cause></cause>
    <res></res>
    <obj></obj>
    '''
    id = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=64, verbose_name='nom du fichier')
    num_phrase = models.BigIntegerField(verbose_name='numéro de la phrase')
    dynamique = models.TextField(verbose_name='dynamique')
    cause = models.TextField(verbose_name='segment annoté cause de la nouvelle')
    res = models.TextField(verbose_name='segment annoté res de la nouvelle')
    obj = models.TextField(verbose_name='segment annoté obj de la nouvelle')



