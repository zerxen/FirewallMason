'''
Created on Jul 2, 2017

@author: havrila
'''
from rest_framework import serializers
from firewall_rules.models import *

'''
#####################
# Serializers for API
#####################
'''
class UserSerializer(serializers.ModelSerializer):    
    """
    Serializer for the User model, we are not providing password for a purpose
    """
    class Meta:
        model = User
        fields = ('id', 'username')
        
class PortSerializer(serializers.ModelSerializer):
    """
    Serializer for the Port model
    """
    class Meta:
        model = Port
        #fields = ('id','protocol', 'range', 'description','number','number2', 'version', 'owner')
        fields = '__all__'   
        
class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model
    """
    class Meta:
        model = Service
        fields = '__all__'   
        
class RuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rule model
    """
    class Meta:
        model = Rule
        fields = '__all__'  
        
                 
