from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, mixins
from firewall_rules.models import *
from .serializers import *
from pprint import pprint
import custom_mixins

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """        
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# ViewSets define the view behavior.
class MixedViewSet(custom_mixins.MasonCreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   #mixins.UpdateModelMixin,
                   #mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    
       


# ViewSets define the view behavior.
class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer   
    

#class MyPortsField(serializers.RelatedField):
#    def to_native(self, value):
#        return { str(value.pk): str(value) }    

# Serializers define the API representation.
      
# ViewSets define the view behavior.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer    
    
# Serializers define the API representation.

      
# ViewSets define the view behavior.
class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer    
         
# ViewSets define the view behavior.
class UserFilteredRuleViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        Logger.debug("UserFilteredRuleViewSet: testing self.request user existence: " +  str(self.request.user))
        return Rule.objects.filter(action='D')
    model = Rule   
    '''queryset has to be empty here''' 
    #queryset = Rule.getUseAllowedObjects(self.request.user)
    serializer_class = RuleSerializer      
    
# ViewSets define the view behavior.
class UserFilteredView(#mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    Return a list of all the existing users begining with filtered.
    
    get:
    Return a list of all the existing users.
    """   

    model = User   
    serializer_class = UserSerializer
    queryset = User.objects.all()
     
    def get_queryset(self):
        Logger.debug("UserFilteredView: testing self.request user existence: " +  str(self.request.user))
        #if self.request.GET['filter'] is not None:
        query_filter=self.request.GET.get('filter', '')
        #query_filter=self.request.GET['filter']
        Logger.debug("UserFilteredView: testing query_filter: " +  query_filter)
        return self.model.objects.filter(username__startswith=query_filter)
        #else:
        #    return self.model.objects.all()

    '''queryset has to be empty here''' 
    #queryset = Rule.getUseAllowedObjects(self.request.user)
    
    
       

