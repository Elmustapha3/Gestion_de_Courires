
# Create your models here.

from django.db import models
from django.contrib.auth.models import User,Group
from datetime import date, datetime


    
class Consigne(models.Model):
    remarque=models.TextField(max_length=70)
    date_consigne=models.DateTimeField()
    
    
    def __str__(self):
        return self.remarque

class Service(models.Model):
    nom=models.CharField(max_length=30)
    division=models.ForeignKey('Division',on_delete=models.CASCADE)


    def __str__(self):
        return self.nom
    
    
class Division(models.Model):
    nom=models.CharField(max_length=30)


    
    
    def __str__(self):
        return self.nom
    

    
    def __str__(self):
        return self.nom
    
class Role(models.Model):

    nom=models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom

    

class Utilisateur(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    identifiant=models.CharField(max_length=10,default='',unique=True)
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=20)
    email=models.EmailField(default='')
    telephone=models.BigIntegerField(max_length=14)
    role=models.ForeignKey('Role',on_delete=models.CASCADE)
    division=models.ForeignKey('Division',on_delete=models.SET_NULL,null=True)
    service=models.ForeignKey('Service',on_delete=models.SET_NULL,null=True,blank=True)

    
    def __str__(self):
        return self.nom


class Nature(models.Model):
    nom=models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom

class Categorie(models.Model):
    nom=models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom

class Courrier(models.Model):
    nature=models.ForeignKey('Nature',on_delete=models.SET_NULL,null=True)
    categorie=models.ForeignKey('Categorie',on_delete=models.SET_NULL,null=True)
    priocourrier = [
        ('',''),
        ('normal','Normal'),
        ('urgent','Urgent'),
        ('très urgent','Très urgent')
    ]
    
    priorite=models.CharField(max_length=30,choices=priocourrier,default='')
    consigne=models.ForeignKey('Consigne',on_delete=models.SET_NULL,null=True)
    autre_consigne=models.CharField(max_length=50,blank=True)
    date_courrier=models.DateField()
    date_arrivee=models.DateField()
    numero_ordre=models.BigIntegerField()
    objet=models.TextField(max_length=70)
    reference=models.CharField(max_length=10)
    

    
    

    
   
    
    
    
class Affectation(models.Model):
    service=models.ForeignKey('Service',on_delete=models.CASCADE)
    date_limite_de_traitement=models.DateField()
    courrier=models.ForeignKey('Courrier',on_delete=models.CASCADE)
    
    @property
    def is_valid1(self):
        if self.date_limite_de_traitement > Courrier.date_arrivee :
            return True
        else:
            return False

    
class Type_contact(models.Model):
    nom=models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom
    
class Contact(models.Model):
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=20)
    adresse=models.TextField(max_length=80)
    code_postal=models.BigIntegerField()
    type=models.ForeignKey('Type_contact',on_delete=models.CASCADE)
    prefecture_province=models.CharField(max_length=30)
     
    def __str__(self):
        return self.nom

    
class Courrierdepart(models.Model):
    numero=models.PositiveIntegerField(max_length=10,unique=True)
    date_courrier=models.DateField()
    type=models.ForeignKey('Nature',on_delete=models.CASCADE)
    destination=models.ForeignKey('Contact',on_delete=models.CASCADE)
    adresse=models.TextField(max_length=50)
    objet=models.TextField(max_length=60)
    