
from django.contrib import admin

# Register your models here.
from courriers.models import Utilisateur,Courrierdepart,Role,Division,Service,Courrier,Categorie,Consigne,Contact,Nature,Affectation,Type_contact


class UtilisateurAdmin(admin.ModelAdmin):
    list_display=('identifiant','nom','prenom','email','role','division','service')
 
admin.site.register(Utilisateur,UtilisateurAdmin)

admin.site.register(Role)
admin.site.register(Type_contact)
class CourrierAdmin(admin.ModelAdmin):
    list_display=('nature','categorie','priorite','date_arrivee','date_courrier',
                  'numero_ordre','objet','reference','consigne','autre_consigne')
admin.site.register(Courrier,CourrierAdmin)



admin.site.register(Categorie)
admin.site.register(Division)

admin.site.register(Nature)
class ConsigneAdmin(admin.ModelAdmin):
    list_display=('remarque','date_consigne')
admin.site.register(Consigne,ConsigneAdmin)
class ContactAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','adresse','code_postal','type','prefecture_province')
admin.site.register(Contact,ContactAdmin)

class AffectationAdmin(admin.ModelAdmin):
    list_display=('courrier','service')
admin.site.register(Affectation,AffectationAdmin)



class ServiceAdmin(admin.ModelAdmin):
    list_display=('nom','division')
admin.site.register(Service,ServiceAdmin)

class CourrierdepartAdmin(admin.ModelAdmin):
    list_display=['numero','date_courrier','type','destination','adresse','objet']
admin.site.register(Courrierdepart,CourrierdepartAdmin)


