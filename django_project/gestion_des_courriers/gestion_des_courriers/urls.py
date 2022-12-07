"""wilaya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from courriers import urls, views
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('courriers/',include('courriers.urls')),
    path('', views.home_view,name="home_view"),
    path('userslogin/', LoginView.as_view(template_name='userslogin.html'),name='userslogin'),
    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('homeadmin/',views.dahsboardadmin,name="homeadmin"),
    path('logout/', LogoutView.as_view(template_name='ind.html')),
    #Admin part#
    path('listcourriersadmin/',views.searchadmin,name="listcourriersadmin"),
    path('registerusers/',views.register_view,name="registerusers"),
    path('listusers/',views.listusers,name="listusers"),
    path('update/<int:id>',views.update,name="update"),
    path('update/updeateuser/<int:id>', views.updateuser, name='updateuser'),
    path('delete/<int:id>',views.delete),
    path('consignes/',views.consigne,name="consignes"),
    path('listconsignes/',views.listconsignes,name="listconsignes"),
    path('deleteconsignes/<int:id>',views.deleteconsigne,name="deleteconsigne"),
    path('listcourriersadmin/',views.listcourriersadmin,name='listcourriersadmin'),
    path('listaffectationsadmin/',views.listaffectationsadmin,name='listaffectationsadmin'),
 
    #DIV PART#
    path('home/',views.dahsboardchefdivision,name="home"),
    path('enregistrer/',views.savecourrier,name="savecourrier"),
    path('affecter/',views.affectercourrier,name="affecter"),
    path('courriersdiv/',views.listcourriers,name="courriersdiv"),
    path('courriers/',views.searchchefdiv,name='courriers'),

    
    path('listaffectationsdiv/',views.listaffectations,name="listaffectationsdiv"),
    path('deleteaff/<int:id>',views.deleteaff,name='deleteaff'),
    path('updatecour/<int:id>',views.courupdate,name="updatecour"),
    path('updatecour/updatecourrier/<int:id>',views.courrierupdate,name="updatecourrier"),
    path('deletecour/<int:id>',views.deletecourrier,name='deletecourrier'),
    path('updateaff/<int:id>',views.affupdate,name='updateaff'),
    path('updateaff/updateaffectation/<int:id>',views.affectationupdate,name='updateaffectation'),
    #chefdeservice
    path('homechefservice/',views.dashboardchefservice,name='dashboardchefservice'),
    path('listcourrierschef/',views.listcourrierschef,name="listcourrierschef"),
    path('listaffectationschef/',views.listaffectationschef,name="listaffectationschef"),
    path('updatecourchef/<int:id>',views.courupdatechef,name='courupdatechef'),
    path('updatecourchef/updatecourrierchef/<int:id>',views.courrierupdatechef,name='courrierupdatechef'),
    path('courrierschef/',views.searchchef,name='courrierschef'),

    #AGENT TRANSMISSION
    path('hometransmission/',views.dahsboardtransmission,name='hometransmission'),
    path('enregistrercontact/',views.addcontact,name='enregistrercontact'),
    path('addtypecontact/',views.addtypecontact,name='addtypecontact'),
    path('courrierstrans/',views.listcourrierstrans,name='courrierstrans'),
    path('contacttrans/',views.listcontacts,name='contacttrans'),
    path('updatec/<int:id>',views.updateco,name='updatec'),
    path('updatec/updatecontact/<int:id>',views.updatecontact,name='updatecontact'),
    path('deletec/<int:id>',views.deletecontact,name='deletec'),
    path('envoyercourrier/',views.envoyercourrier,name='envoyercourrier'),
    path('courriersenv/',views.courriersenv,name='courriersenv'),
    path('updatecourtrans/<int:id>',views.updatecourtrans,name="updatecourtrans"),
    path('updatecourtrans/updatecourtransmission/<int:id>',views.updatecourriertrans,name="updatecourtransmission"),
    path('deletecourenv/<int:id>',views.deletecourenv,name="deletecourenv"),
    path('courrierstr/',views.searchtrans,name='courrierstr'),
    
    #AGENT SERVICE
    path('homeagentservice/',views.dahsboardagent,name='homeagentservice'),
    path('courriersagent/',views.listcourriersagent,name='courriersagent'),
    path('affectationsagent/',views.affectationsagent,name='affectationsagent'),
    path('courriersag/',views.searchagent,name="courriersag"),
    
    
    

]




