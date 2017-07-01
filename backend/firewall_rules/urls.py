from django.conf.urls import url
#from firewall_rules.views_classes.RulesView import RulesView
from firewall_rules.views_classes import LdapView
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from firewall_rules.rest_api_experiments.rest_api import *
from firewall_rules.rest_api_experiments.rest_api_jobs import *
from firewall_rules.rest_api_experiments.ExtendedRouter import ExtendedRouter
from django.contrib.auth.decorators import login_required
from rest_framework.documentation import include_docs_urls


from . import views

from rest_framework.authtoken import views as rest_framework_views

app_name = 'firewall_rules_namespace'


'''
REST API ROUTER
'''
# Routers provide an easy way of automatically determining the URL conf.
router = ExtendedRouter()
router.register(r'users', UserViewSet)
router.register(r'users2', MixedViewSet)
router.register(r'users-search', UserFilteredView)
router.register(r'ports', PortViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'rules', RuleViewSet)
router.register(r'filtered_rules', UserFilteredRuleViewSet,'filtered_rules')
router.register(r'version', VersionsList,'version')
#router.register(r'user-details', UserViewSet)


'''
 REST API VIEWS
'''
urlpatterns = [
    
    url(r'^api/', include(router.urls, namespace='api')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    
    #url(r'^api/version/$', VersionsList.as_view()),
    #url(r'^api/version/(?P<pk>[0-9]+)/$', VersionDetail.as_view()),
    url(r'^docs/', include_docs_urls(title='Firewall Mason API')), 

]

'''
 REGULAR VIEWS
'''
urlpatterns = urlpatterns + [

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


