from dataclasses import fields
from django import forms
from django.contrib.auth.models import User,Group
from courriers.models import Affectation, Consigne, Contact, Courrier, Courrierdepart, Role, Type_contact, Utilisateur

class LoginusersForm(forms.ModelForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=True)
    class Meta:
        model=User
        fields = ['username','password','groups']
        
        

   
class Registration(forms.ModelForm):
    nom=forms.CharField(max_length=20,required=True)
    prenom=forms.CharField(max_length=20,required=True)
    email=forms.EmailField(required=True)
    telephone=forms.TextInput(attrs={'class':'form-control'})
    identifiant=forms.CharField(label="Identifiant" ,max_length=10,required=True)
    
    class Meta:
        model=Utilisateur
        fields=['identifiant','nom','prenom','email','role','telephone','division','service']

class consigneform(forms.ModelForm):
    date_consigne=forms.DateTimeField(label="Entrer une date de consigne",widget=forms.SelectDateWidget)
    remarque=forms.CharField(max_length=80)
    class Meta:
        model=Consigne
        fields=['remarque','date_consigne']
        
class courrierform(forms.ModelForm):
    date_courrier=forms.DateField(label="choisir une date courrier",widget=forms.SelectDateWidget)
    date_arrivee=forms.DateField(label="choisir une date d'arrivée du courrier",widget=forms.SelectDateWidget)
    numero_ordre=forms.NumberInput()
    objet=forms.CharField()
    reference=forms.CharField()
    
    
    class Meta:
        model=Courrier
        fields=['nature','categorie','priorite','date_courrier','date_arrivee',
                'numero_ordre','objet','reference','consigne','autre_consigne']
        
class affectationform(forms.ModelForm):
    date_limite_de_traitement=forms.DateField(label="choisir une date d'affectation",widget=forms.SelectDateWidget)
    class Meta:
        model=Affectation
        fields=['courrier','service','date_limite_de_traitement']
        

class Contactform(forms.ModelForm):
    nom=forms.CharField(max_length=20,required=True)
    prenom=forms.CharField(max_length=20,required=False)
    adresse=forms.CharField(max_length=80)
    code_postal=forms.IntegerField(max_value=100000)
    prefecture_province=forms.CharField(max_length=20)

     
    class Meta:
        model=Contact
        fields=['nom','prenom','adresse','code_postal','type','prefecture_province']
        
class Type_contactform(forms.ModelForm):
    nom=forms.CharField(max_length=20,required=True)
    class Meta:
        model=Type_contact
        fields=['nom']
        
class Courrierdepartform(forms.ModelForm):
    numero=forms.NumberInput()
    date_courrier=forms.DateField(widget=forms.SelectDateWidget)
    adresse=forms.CharField(max_length=50)
    objet=forms.CharField(max_length=50)
    class Meta:
        model=Courrierdepart
        fields=['numero','date_courrier','type','destination','adresse','objet']
        
