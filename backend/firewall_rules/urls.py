from django.conf.urls import url
#from firewall_rules.views_classes.RulesView import RulesView
from firewall_rules.views_classes import LdapView
from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'firewall_rules_namespace'

'''
 REGULAR VIEWS
'''
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^ldap_auth/$', LdapView.ldap_auth, name='ldap_auth'),
    url(r'^about/$', views.about, name='about'),
    url(r'^requestaccess/$', views.request_access, name='requestaccess'),
    
    url(r'^version_control/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.VersionControlView.as_view()), name='version_control'),       
        
    url(r'^rules/$', login_required(views.RulesView.as_view()), name='rules'),
    url(r'^rules/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/$', login_required(views.FirebrickRuleDetailView.as_view()), name='rules_detail'),    
    # Experimental LDAP authentication
    url(r'^firewall_configuration/$', login_required(views.firewall_configuration), name='firewall_configuration'),
    url(r'^ports/$', login_required(views.PortsView.as_view()), name='ports'),
    url(r'^ports/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickPortDetailView.as_view()), name='ports_detail'),
    url(r'^services/$', login_required(views.ServicesView.as_view()), name='services'),
    url(r'^services/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickServiceDetailView.as_view()), name='services_detail'),
    url(r'^locations/$', login_required(views.LocationsView.as_view()), name='locations'),
    url(r'^locations/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickLocationDetailView.as_view()), name='locations_detail'), 
    url(r'^atomicnetworkobjects/$', login_required(views.AtomicNetworkObjectView.as_view()), name='atomicnetworkobjects'),
    url(r'^atomicnetworkobjects/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickAtomicNetworkObjectDetailView.as_view()), name='atomicnetworkobjects_detail'),       
    #StaticNetworkObjectGroup
    url(r'^staticnetworkobjectgroups/$', login_required(views.StaticNetworkObjectGroupView.as_view()), name='staticnetworkobjectgroups'),
    url(r'^staticnetworkobjectgroups/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickStaticNetworkObjectGroupDetailView.as_view()), name='staticnetworkobjectgroups_detail'),       
    #SystemMap
    url(r'^systemmaps/$', login_required(views.SystemMapView.as_view()), name='systemmaps'),
    url(r'^systemmaps/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickSystemMapDetailView.as_view()), name='systemmaps_detail'),  
    #NetworkObjectsToLocations
    url(r'^networkobjectlocations/$', login_required(views.AtomicNetworkObjectToLocationBindView.as_view()), name='atomicnetworkobjecttolocationbinds'),
    url(r'^networkobjectlocations/(?P<pk>[0-9]+)/(?P<command>[a-z]+)/', login_required(views.FirebrickAtomicNetworkObjectToLocationBindDetailView.as_view()), name='atomicnetworkobjecttolocationbinds_detail'),      
 
    

    
]

#


