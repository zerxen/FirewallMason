from django.conf.urls import url
from firewall_rules.views_classes import LdapView
from django.conf.urls import url, include
from django.contrib.auth.models import User

from views_and_serializers.routers import ExtendedRouter
from rest_framework import routers
from rest_framework.authtoken import views as rest_framework_views
from views_and_serializers.view_sets import *
from views_and_serializers.api_views import *
from django.contrib.auth.decorators import login_required
from rest_framework.documentation import include_docs_urls

'''
 ViewSETs Router
'''
router = ExtendedRouter()
#router.register(r'users', UserViewSet,'users')
#router.register(r'ports', PortViewSet,'ports')
router.register(r'users', MixedViewSet,'users')
#router.register(r'ports', PortList,'ports')
#router.register(r'ports', MyPortViewSet,'ports')



'''
 REGULAR URLs
'''
urlpatterns = [
    #url(r'^', include(router.urls)),
    url(r'^', include_docs_urls(title='FirewallMason APIs')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),  
    
    url(r'^ports/$', PortList.as_view(), name='ports'),
    url(r'^ports/(?P<pk>[0-9]+)/', PortDetail.as_view(), name='ports_detail'),
    
    
]



