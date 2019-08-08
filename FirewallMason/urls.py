"""FirewallMason URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from firewall_rules.views import index as firewall_rules_index
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^accounts/login/$', auth_views.login, name='login'),
    #TODO placeholder
    url(r'^accounts/profile/$', firewall_rules_index , name='profile'),
    
    #url(r'^logout/$','django.contrib.auth.views.logout',name='logout',kwargs={'next_page': '/'}),        
    
    #url(r'^polls/', include('polls.urls')),
    url(r'^firewall_rules/', include('firewall_rules.urls')),
    
    url(r'^docs/', include_docs_urls(title='Firewall Mason API')), 
    
    
]
