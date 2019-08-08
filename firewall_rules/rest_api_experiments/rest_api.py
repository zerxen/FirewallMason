from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, mixins
from firewall_rules.models import *
from pprint import pprint

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-details")
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-detail")
    
    class Meta:
        model = User
        #fields = ('url', 'username', 'email', 'is_staff')
        #fields = ('username', 'email', 'is_staff')
        #fields = '__all__'
        fields = ('id', 'username')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# ViewSets define the view behavior.
class MixedViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    
       
    
# Serializers define the API representation.
class PortSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-details")
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-detail")
    
    class Meta:
        model = Port
        #fields = ('url', 'username', 'email', 'is_staff')
        fields = ('protocol', 'range', 'description','number','number2')


# ViewSets define the view behavior.
class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer   
    

#class MyPortsField(serializers.RelatedField):
#    def to_native(self, value):
#        return { str(value.pk): str(value) }    

# Serializers define the API representation.
class ServiceSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-details")
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-detail")
    #ports = serializers.ManyRelatedField(source="ports")
    #ports = MyPortsField(many=True,queryset=Port.objects.all())
    
    class Meta:
        model = Service
        #fields = ('url', 'username', 'email', 'is_staff')
        #fields = ('name','ports')
        fields = '__all__'
      
# ViewSets define the view behavior.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer    
    
# Serializers define the API representation.
class RuleSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-details")
    #url = serializers.HyperlinkedIdentityField(view_name="firewall_rules_namespace:user-detail")
    #ports = serializers.ManyRelatedField(source="ports")
    #ports = MyPortsField(many=True,queryset=Port.objects.all())
    
    class Meta:
        model = Rule
        #fields = ('url', 'username', 'email', 'is_staff')
        #fields = ('name','ports')
        fields = '__all__'
      
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
        #pprint(self.request.method)
        query_filter=self.request.GET['filter']
        Logger.debug("UserFilteredView: testing query_filter: " +  query_filter)
        return self.model.objects.filter(username__startswith=query_filter)

    '''queryset has to be empty here''' 
    #queryset = Rule.getUseAllowedObjects(self.request.user)
       

