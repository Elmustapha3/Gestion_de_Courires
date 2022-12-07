from fileinput import filename
import re
from django.urls import reverse
from django.contrib import messages
from django import views
from django.template import loader
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode

from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group,User
from courriers.forms import Contactform, Courrierdepartform, LoginusersForm,Registration, Type_contactform, affectationform, consigneform, courrierform
from django.forms import ValidationError
from django.contrib.auth import login,authenticate

from courriers.models import Affectation, Consigne, Contact, Courrier, Courrierdepart, Role, Utilisateur
# Create your views here.

def home_view(request):
    return render(request,'ind.html')

def login_view(request):
    return render(request,'login.html')

@login_required(login_url='home')
def dahsboardchefdivision(request):
    num_courrier=Courrier.objects.all().count()
    num_affectation=Affectation.objects.all().count()
    context={
        'num_courrier':num_courrier,
        'num_affectation':num_affectation
    }
    return render(request,'dashboardchef.html',context=context)

@login_required(login_url='homeadmin')
def dahsboardadmin(request):
    num_courrier=Courrier.objects.all().count()
    num_affectation=Affectation.objects.all().count()
    num_consigne=Consigne.objects.all().count()
    num_utilisateur=Utilisateur.objects.all().count()
    context={
        'num_courrier':num_courrier,
        'num_affectation':num_affectation,
        'num_consigne':num_consigne,
        'num_utilisateur':num_utilisateur,
    }
    return render(request,'dashboardadmin.html',context=context)

@login_required(login_url='hometransmission')
def dahsboardtransmission(request):
    num_courrier=Courrierdepart.objects.all().count()
    num_contact=Contact.objects.all().count()
    context={
        'num_courrier':num_courrier,
        'num_contact':num_contact,
        
    }
    return render(request,'dashboardtransmission.html',context=context)

@login_required(login_url='homechefservice')
def dashboardchefservice(request):
    num_courrier=Courrier.objects.all().count()
    num_affectation=Affectation.objects.all().count()
    context={
        'num_courrier':num_courrier,
        'num_affectation':num_affectation
    }
    return render(request,'dashboardchefservice.html',context=context)


@login_required(login_url='homeagentservice')
def dahsboardagent(request):
    num_courrier=Courrier.objects.all().count()
    num_affectation=Affectation.objects.all().count()
   
    context={
        'num_courrier':num_courrier,
        'num_affectation':num_affectation,
    }
    return render(request,'dashboardagent.html',context=context)

def is_admin(user):
    return user.groups.filter(name='ADMINISTRATEUR').exists()

def is_chefdivision(user):
    return user.groups.filter(name='DIVISION SG').exists()

def is_agenttransmission(user):
    return user.groups.filter(name='TRANSMISSION').exists()

def is_chefservice(user):
    return user.groups.filter(name='SERVICE SG').exists()
def is_agentservice(user):
    return user.groups.filter(name='AGENT').exists()


def afterlogin_view(request):
    form=LoginusersForm()
    msg=None
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_active:
                login(request,user)
                
                if is_admin(request.user):
                    return render(request,'dashboardadmin.html',{'user':user.get_username})
                
                elif is_chefdivision(request.user):
                    return render(request,'chefdivisionafter.html',{'user':user.get_username})       
                
                elif is_agenttransmission(request.user):
                    return render(request,'agenttransmissionafter.html',{'user':user.get_username})
                
                elif is_chefservice(request.user):
                    return render(request,'dashboardchefservice.html',{'user':user.get_username})
                
                elif is_agentservice(request.user):
                    return render(request,'dashboardagent.html',{'user':user.get_username})
                    
        else:
            form=LoginusersForm()
            msg='Username or Password incorrect'
            
             

            
            
    return render(request,'userslogin.html',{'form':form,'msg':msg})

    
@login_required(login_url='registerusers')
    
def register_view(request):
    form=LoginusersForm()
    form1=Registration()
    mydict={'form':form,'form1':form1}
    if request.method=='POST':
        form=LoginusersForm(request.POST)
        form1=Registration(request.POST)
        if form.is_valid() and form1.is_valid():
            user=form.save()
            user.set_password(user.password)
            utilisateur=form1.save(commit=False)
            utilisateur.user=user
            utilisateur.save()
            user.save()
        else:
            form=LoginusersForm()
            form1=Registration()
         
        

    return render(request,'registerusers.html',context=mydict)

@login_required(login_url='listusers')

def listusers(request):
    liste1=Utilisateur.objects.all()
    liste2=User.objects.all()
    return render(request,'listusers.html',{'liste1':liste1,'liste2':liste2})

@login_required(login_url='update')
def update(request,id):
    utilisateur=Utilisateur.objects.get(id=id)
    formuser=Registration(instance=utilisateur)
    template=loader.get_template('update.html')
    context={
        'utilisateur':utilisateur,
        'formuser':formuser,
       
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='updateuser')
def updateuser(request,id):
    form=Registration(request.POST)
    utilisateur=Utilisateur.objects.get(id=id)
    if request.method=="POST":
        formc=Registration(request.POST,instance=utilisateur)
        formc.save()
    return HttpResponseRedirect(reverse('listusers'))
        
    
@login_required(login_url='delete')
    
def delete(request,id):
    utilisateurs=Utilisateur.objects.get(id=id)    
    utilisateurs.delete()

    return redirect("/listusers")

@login_required(login_url='consignes')
def consigne(request):
    formc=consigneform()
    if request.method=='POST':
        formc=consigneform(request.POST)
        if formc.is_valid():
            consigne=formc.save()
        else:
            formc=consigneform()
            
    return render(request,'addconsigne.html',{'formc':formc})


#Admin
@login_required(login_url='listconsignes')
def listconsignes(request):
    listc=Consigne.objects.all()
    return render(request,'listconsignes.html',{'listc':listc})
#Admin
@login_required(login_url='deleteconsignes')
def deleteconsigne(request,id):
    consigne=Consigne.objects.get(id=id)    
    consigne.delete()
    return redirect("/listconsignes")


@login_required
def searchadmin(request):
    if 'q' in request.GET:
        q=request.GET['q']
        courrier_list=Courrier.objects.filter(reference__icontains=q)
    else:
        courrier_list=Courrier.objects.all()
    context={
       
        'courrier_list':courrier_list,
    }
    return render(request,'listcourriersadmin.html',context=context)
                
            
@login_required(login_url='listcourriersadmin') 
def listcourriersadmin(request):
    courrier_list = Courrier.objects.all()
    
    return render(request,'listcourriersadmin.html',{'courrier_list':courrier_list})


@login_required(login_url='listaffectationsadmin')
def listaffectationsadmin(request):
    formaffect=Affectation.objects.all()
    return render(request,'listaffectationsadmin.html',{'formaffect':formaffect})

#Division

@login_required
def searchchefdiv(request):
    if 'p' in request.GET:
        p=request.GET['p']
        listcourriers=Courrier.objects.filter(reference__icontains=p)
    else:
        listcourriers=Courrier.objects.all()
    context={
       
        'listcourriers':listcourriers,
    }
    return render(request,'listcourriers.html',context=context)

@login_required
def searchagent(request):
    if 'p' in request.GET:
        p=request.GET['p']
        listcourriersagent=Courrier.objects.filter(reference__icontains=p)
    else:
        listcourriersagent=Courrier.objects.all()
    context={
       
        'listcourriersagent':listcourriersagent,
    }
    return render(request,'listcourriersagent.html',context=context)


@login_required(login_url='affecter')
def affectercourrier(request):
    formaf=affectationform()
    if request.method=='POST':
        formaf=affectationform(request.POST)
        if formaf.is_valid():
            courrier=formaf.save()
        else:
            formaf=affectationform()
            
    return render(request,'affectercourrier.html',{'formaf':formaf})

@login_required(login_url='enregistrer')
def savecourrier(request):
    formcour=courrierform()
    if request.method=='POST':
        formcour=courrierform(request.POST)
    
        if formcour.is_valid():
            courrier=formcour.save()
        else:
            formcour=courrierform()
            
    return render(request,'addcourrier.html',{'formcour':formcour})

@login_required(login_url='courriersdiv')
def listcourriers(request):
    listcourriers=Courrier.objects.all()
    return render(request,'listcourriers.html',{'listcourriers':listcourriers})

@login_required(login_url='listaffectationsdiv')
def listaffectations(request):
    formaffect=Affectation.objects.all()
    return render(request,'listaffectations.html',{'formaffect':formaffect})

@login_required(login_url='deleteaff')
def deleteaff(request,id):
    affectation=Affectation.objects.get(id=id)    
    affectation.delete()
    return redirect("/listaffectationsdiv")

@login_required(login_url='updatecour')
def courupdate(request,id):
    courrier=Courrier.objects.get(id=id)
    formc=courrierform(instance=courrier)
    template=loader.get_template('updatecourrier.html')
    context={
        'formc':formc,
        'courrier':courrier
    
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='updatecourrier')
def courrierupdate(request,id):
    courrier=Courrier.objects.get(id=id)
    if request.method=="POST":
        formc=courrierform(request.POST,instance=courrier)
        formc.save()
    return HttpResponseRedirect(reverse('courriersdiv'))

@login_required(login_url='deletecourrier')
def deletecourrier(request,id):
    courrier=Courrier.objects.get(id=id)
    courrier.delete()
    return redirect("/courriersdiv")
    
@login_required(login_url='updateaff')
def affupdate(request,id):
    affectation=Affectation.objects.get(id=id)
    forma=affectationform(instance=affectation)
    template=loader.get_template('updateaffectation.html')
    context={
        'forma':forma,
        'affectation':affectation
    
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='updateaffectation')
def affectationupdate(request,id):
    affectation=Affectation.objects.get(id=id)
    if request.method=="POST":
        forma=affectationform(request.POST,instance=affectation)
        forma.save()
    return HttpResponseRedirect(reverse('listaffectationsdiv'))

#Chef de service

@login_required(login_url='listcourrierschef')

def listcourrierschef(request):
    listcourriers=Courrier.objects.all()
    return render(request,'listcourrierschef.html',{'listcourriers':listcourriers})

@login_required(login_url='listaffectationschef')
def listaffectationschef(request):
    formaffect=Affectation.objects.all()
    return render(request,'listaffectationschef.html',{'formaffect':formaffect})

@login_required(login_url='courupdatechef')
def courupdatechef(request,id):
    courrier=Courrier.objects.get(id=id)
    formc=courrierform(instance=courrier)
    template=loader.get_template('updatecourrierchef.html')
    context={
        'formc':formc,
        'courrier':courrier
    
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='courrierupdatechef')
def courrierupdatechef(request,id):
    courrier=Courrier.objects.get(id=id)
    if request.method=="POST":
        formc=courrierform(request.POST,instance=courrier)
        formc.save()
    return HttpResponseRedirect(reverse('listcourrierschef'))

#AGENT TRANSMISSION
@login_required
def searchtrans(request):
    if 'p' in request.GET:
        p=request.GET['p']
        listcourriers=Courrier.objects.filter(reference__icontains=p)
    else:
        listcourriers=Courrier.objects.all()
    context={
       
        'listcourriers':listcourriers,
    }
    return render(request,'listcourrierstrans.html',context=context)

@login_required
def searchchef(request):
    if 'p' in request.GET:
        p=request.GET['p']
        listcourriers=Courrier.objects.filter(reference__icontains=p)
    else:
        listcourriers=Courrier.objects.all()
    context={
       
        'listcourriers':listcourriers,
    }
    return render(request,'listcourrierschef.html',context=context)

@login_required(login_url='enregistrercontact')
def addcontact(request):
    formcontact=Contactform()
    if request.method=='POST':
        formcontact=Contactform(request.POST)
        if formcontact.is_valid():
            contact=formcontact.save()
        else:
            formcontact=Contactform()
            
    return render(request,'addcontact.html',{'formcontact':formcontact})

@login_required(login_url='addtypecontact')
def addtypecontact(request):
    formtypec=Type_contactform()
    if request.method=='POST':
        formtypec=Type_contactform(request.POST)
        if formtypec.is_valid():
            type=formtypec.save()
        else:
            formtypec=Type_contactform()            
    return render(request,'addtypecontact.html',{'formtypec':formtypec})


@login_required(login_url='courrierstrans')
def listcourrierstrans(request):
    listcourriers=Courrier.objects.all()
    return render(request,'listcourrierstrans.html',{'listcourriers':listcourriers})


@login_required(login_url='contacttrans')
def listcontacts(request):
    listcontacts=Contact.objects.all()
    return render(request,'listcontacts.html',{'listcontacts':listcontacts})

@login_required(login_url='updatec')
def updateco(request,id):
    contact=Contact.objects.get(id=id)
    formcontact=Contactform(instance=contact)
    template=loader.get_template('updatecontact.html')
    context={
        'formcontact':formcontact,
        'contact':contact,
    
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='updatecontact')
def updatecontact(request,id):
    contact=Contact.objects.get(id=id)
    if request.method=="POST":
        formcontact=Contactform(request.POST,instance=contact)
        formcontact.save()
    return HttpResponseRedirect(reverse('contacttrans'))

@login_required(login_url='deletec')
def deletecontact(request,id):
    contact=Contact.objects.get(id=id)
    contact.delete()
    return redirect("/contacttrans")

@login_required(login_url='envoyercourrier')
def envoyercourrier(request):
    formcourrierdep=Courrierdepartform()
    if request.method=='POST':
        formcourrierdep=Courrierdepartform(request.POST)
        if formcourrierdep.is_valid():
            courrierdep=formcourrierdep.save()
        else:
            formcourrierdep=Courrierdepartform()
            
    return render(request,'sendcourrier.html',{'formcourrierdep':formcourrierdep})

@login_required(login_url='courriersenv')
def courriersenv(request):
    formcourrierdep=Courrierdepart.objects.all()
    return render(request,'courriersenv.html',{'formcourrierdep':formcourrierdep})

@login_required(login_url='updatecourtrans')
def updatecourtrans(request,id):
    courrier=Courrierdepart.objects.get(id=id)
    formcourrier=Courrierdepartform(instance=courrier)
    template=loader.get_template('updatecourriertrans.html')
    context={
        'formcourrier':formcourrier,
        'courrier':courrier
    
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='courriersenv')
def updatecourriertrans(request,id):
    courrier=Courrierdepart.objects.get(id=id)
    if request.method=="POST":
        formc=Courrierdepartform(request.POST,instance=courrier)
        formc.save()
    return HttpResponseRedirect(reverse('courriersenv'))

@login_required(login_url='deletecourenv')
def deletecourenv(request,id):
    courrier=Courrierdepart.objects.get(id=id)
    courrier.delete()
    return redirect("/courriersenv")

#AGENT SERVICE
@login_required(login_url='courriersagent')
def listcourriersagent(request):
    listcourriersagent=Courrier.objects.all()
    return render(request,'listcourriersagent.html',{'listcourriersagent':listcourriersagent})

@login_required(login_url='affectationsagent')
def affectationsagent(request):
    affectation=Affectation.objects.all()
    return render(request,'listaffectationsagent.html',{'affectation':affectation})

