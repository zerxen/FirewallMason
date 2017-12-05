from __future__ import unicode_literals
from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.
import datetime
import re

from django.db import models
from django.utils import timezone;

'''
TOKEN OVERRIDE FOR USERS TO GET TOKEN AFTER SAVE (e.g. user creation) FUNCTION
'''
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

'''
    DEFAULT GROUP ID 
'''
# This should be set for group ID of the group that will OWN everything once 
# foreign key is deleted, something lake "orphaned group"
DEFAULT_OWNER_GROUP = 1

'''
    DB LOG
'''
class Logger(models.Model):
    date = models.DateTimeField('date published')
    log_text = models.CharField(max_length=5000)
    
    OBJECT_TYPES = (
        (0, 'emergencies'),
        (1, 'alerts'),
        (2, 'critical'),
        (3, 'errors'),
        (4, 'warnings'),
        (5, 'notifications'),
        (6, 'informational'),
        (7, 'debugging'),
    )    
    severity = models.PositiveSmallIntegerField(default=6)    

    @staticmethod
    def debug(log_text):
        now = timezone.now()
        log = Logger(date=now,log_text=log_text)
        log.severity = 7
        log.save() 
        print("LOG["+ str(log.severity) + "]: " + log_text)
    
    @staticmethod
    def log(log_text):
        now = timezone.now()
        log = Logger(date=now,log_text=log_text)
        log.save() 
        print("LOG["+ str(log.severity) + "]: " + log_text)

'''
VERSION STATE
'''
class CurrentVersionState(models.Model):
    '''
    PK/ID will be considered version state since it is incrementing integer by default
    ''' 
    date_created         = models.DateTimeField('date created',blank=True, default=None, null=True)
    date_review_started  = models.DateTimeField('date created',blank=True, default=None, null=True)
    date_approved        = models.DateTimeField('date created',blank=True, default=None, null=True)
    comment     = models.CharField(max_length=5000)  
    
    ''' version control states'''
    INIT = 0
    APPROVED = 1
    EDITING = 2
    REVIEW = 3

    VERSION_STATE = (
        (EDITING, 'Editing & Unlocked'),
        (REVIEW, 'Review & Locked'),
        (APPROVED, 'Approved & Locked')
    )
    version_states = models.PositiveSmallIntegerField(
        choices=VERSION_STATE,
        default=0, #Because initialization will increment to 1
    )
    
    '''    
    VERSION_STATE = (
        (0, 'approved & locked'),
        (1, 'edited & unlocked'),
        (2, 'review & locked'),        
    )
    version_states = models.PositiveSmallIntegerField(default=0) 
    '''
    '''
    This works to quickly get boolean from state
    '''
    @staticmethod
    def lastapproved():
        lastVersionState = CurrentVersionState.objects.latest('id')
        if lastVersionState.version_states == 0:
            return True
        else:
            return False 
        
    @staticmethod
    def addcomment(comment,user):
        version_control = CurrentVersionState.objects.latest('id') 
        version_control.comment = version_control.comment + "\n" +  str(user) + ": " + str(comment);
        Logger.log("Version controll add comment to " + str(version_control.pk) + " by " + str(user) + ":" + str(comment))
        version_control.save() 
        
    @staticmethod
    def getlatest():
        return CurrentVersionState.objects.latest('id')               

    @staticmethod
    def increase(User):
        comment = "Created by "+ User.username
        now = timezone.now()
        version = CurrentVersionState(date_created=now,comment=comment)
        version.version_states = CurrentVersionState.EDITING
        version.save()
        Logger.log("New version create attempt by user " + User.username)
        
    @staticmethod
    def approvetimestamp():      
        current_version = CurrentVersionState.objects.filter(pk=CurrentVersionState.getlastversionnumber()).get()       
        current_version.date_approved = timezone.now()
        current_version.save()
        Logger.debug("CurrentVersionState approver timestamp for version " + str(CurrentVersionState.getlastversionnumber()) + " date " + str(current_version.date_review_started)) 
        
    @staticmethod
    def edittimestamp():      
        current_version = CurrentVersionState.objects.filter(pk=CurrentVersionState.getlastversionnumber()).get()         
        current_version.date_review_started = timezone.now()
        current_version.save()
        Logger.debug("CurrentVersionState editing start timestamp for version " + str(CurrentVersionState.getlastversionnumber()) + " date " + str(current_version.date_review_started))                
        
  
    @staticmethod
    def getlastversionnumber():
        return CurrentVersionState.objects.latest('id').id
            
    
    @staticmethod
    def cloneDB():
        '''
        Let's start cloning!
        '''
        
        # 1 - AtomicNetworkObject
        atomicnetworkobjects = AtomicNetworkObject.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for atomicnetworkobject in atomicnetworkobjects:
            AtomicNetworkObject.clone(atomicnetworkobject.id)
            
        # 2 - Location Reference
        locaitonreferences = LocationReference.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for locaitonreference in locaitonreferences:
            LocationReference.clone(locaitonreference.id)   
            
        # 3 - Ports
        ports = Port.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for port in ports:
            Port.clone(port.id) 
            
        # 4 - Service
        services = Service.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for service in services:
            Service.clone(service.id)    
            
        # 5 - StaticNetworkObjectGroup
        staticnetworkgroups = StaticNetworkObjectGroup.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for staticnetworkgroup in staticnetworkgroups:
            StaticNetworkObjectGroup.clone(staticnetworkgroup.id)  
            
        # 6 - AtomicNetworkObjectToLocationBind
        atomicnetworkobjectstolocations = AtomicNetworkObjectToLocationBind.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for atomicnetworkobjectstolocation in atomicnetworkobjectstolocations:
            AtomicNetworkObjectToLocationBind.clone(atomicnetworkobjectstolocation.id)     
            
        # 7 - SystemMap
        systemmaps = SystemMap.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for systemmap in systemmaps:
            SystemMap.clone(systemmap.id)      
            
        # 8 - Rules
        rules = Rule.objects.filter(version=CurrentVersionState.getlastversionnumber())
        for rule in rules:
            Rule.clone(rule.id)                                                                    
            
            
        return 0;
          

'''
  GROUP EXTENSION
'''
class GroupExtension(models.Model):
    
    ''' Generic group information '''
    email = models.EmailField(max_length=200)
    description = models.CharField(max_length=1000,blank=True)
    prefix = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.prefix + "_" + str(self.group)
    
    ''' Group permissions '''    
    promiscuous = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    approvers = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    
    @staticmethod
    def getGroupExtensionForUser(user):
        print("DEBUG: " + str(user.id));
        group_extension_list = []
        for group in user.groups.all():
            print("GROUP:" + group.name)
            group_extension = GroupExtension.objects.get(group=group)
            if group_extension is not None:
                group_extension_list.append(group_extension)
        return group_extension_list
    
    @staticmethod
    def bUserInAdminGroup(user):
        print("DEBUG: " + str(user.id));
        group_extension_list = []
        for group in user.groups.all():
            print("GROUP:" + group.name)
            group_extension = GroupExtension.objects.get(group=group)
            if group_extension.admin :
                return True;
            
        return False         
        
           
    
class OwnerControl(models.Model):
    class Meta:
        abstract = True
    
    # Owner
    owner = models.ForeignKey(GroupExtension, on_delete=models.CASCADE, default=DEFAULT_OWNER_GROUP)    
    
    @classmethod
    def getUseAllowedObjects(cls, User):
        print("DEBUG: User is authenticated")
        print("DEBUG: " + str(User.id));
        print("DEBUG: " + User.username);
        print("DEBUG: " + User.email);
        Objects = [];
        for group in User.groups.all():
            print("GROUP:" + group.name)
            group_extension = GroupExtension.objects.get(group=group)
            print("GROUP_EXTENSION:" + str(group_extension))
            if group_extension is not None:
                for object in cls.objects.filter(owner=group_extension).order_by('-id'):
                    object.allow_edit = True
                    Objects.append(object)   
                
        return Objects
    
    @classmethod
    def getPromiscuousObjects(cls):
        Objects = [];
        for group_extension in GroupExtension.objects.all():
            print("GROUP_EXTENSION:" + str(group_extension))
            if group_extension is not None and group_extension.promiscuous:
                for object in cls.objects.filter(owner=group_extension).order_by('-id'):
                    object.allow_edit = False
                    Objects.append(object)   
                
        return Objects 

''' HELPER FUNCTION TO VERSION AND OWNER CONTROL '''    
def lastVersionForDefault():
    return CurrentVersionState.getlastversionnumber()  
    
class VersionAndOwnerControl(OwnerControl):
    class Meta:
        abstract = True
    version     = models.PositiveIntegerField(default=lastVersionForDefault) 
    successor   = models.ForeignKey("self", on_delete=models.SET_NULL,default=None,null=True, blank=True,related_name='next_version')
    predecessor  = models.ForeignKey("self", on_delete=models.SET_NULL,default=None,null=True, blank=True,related_name='previous_version')
    
    @classmethod
    def getUseAllowedObjects(cls, User):
        print("DEBUG: User is authenticated")
        print("DEBUG: " + str(User.id));
        print("DEBUG: " + User.username);
        print("DEBUG: " + User.email);
        Objects = [];
        for group in User.groups.all():
            print("GROUP:" + group.name)
            group_extension = GroupExtension.objects.get(group=group)
            print("GROUP_EXTENSION:" + str(group_extension))
            if group_extension is not None:
                Logger.debug("getUseAllowedObjects group_extension: " + str(group_extension))
                version = CurrentVersionState.getlastversionnumber()
                Logger.debug("getUseAllowedObjects CurrentVersionState.getlastversionnumber(): " + str(version))
                for object in cls.objects.filter(owner=group_extension,version=version).order_by('id'):
                    object.allow_edit = True
                    Objects.append(object)   
                
        return Objects 
    
    @classmethod
    def getPromiscuousObjects(cls):
        Objects = [];
        for group_extension in GroupExtension.objects.all():
            print("GROUP_EXTENSION:" + str(group_extension))
            if group_extension is not None and group_extension.promiscuous:
                version = CurrentVersionState.getlastversionnumber()
                Logger.debug("getPromiscuousObjects CurrentVersionState.getlastversionnumber(): " + str(version))
                for object in cls.objects.filter(owner=group_extension,version=version).order_by('-id'):
                    object.allow_edit = False
                    Objects.append(object)   
                
        return Objects           
    
class ApprovalAndVersionAndOwnerControl(VersionAndOwnerControl):
    class Meta:
        abstract = True
    approved    = models.BooleanField(default=False);
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL,default=None,null=True, blank=True,related_name='approved_by')
    edited_by   = models.ForeignKey(User, on_delete=models.SET_NULL,default=None,null=True, blank=True,related_name='edited_by')
    
    rejected    = models.BooleanField(default=False);
    rejected_reason = models.CharField(max_length=1000,default='',blank=True)
    

    @property
    def can_be_deleted(self):
        if (self.approved and self.successor is not None):
            return True
        else:
            return False  
        
                  

  
  

'''
  Datacenter references for objects
'''
class LocationReference(VersionAndOwnerControl): 
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,blank=True)
    prefix = models.CharField(max_length=100)   
    
    def __str__(self):
        return "[" + self.prefix + "] " + str(self.name)
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning LocationReference ID: " + str(objectid))                   
        # creating clone
        clone = LocationReference.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;      
        # NEW RULE PRACTICALLY
        clone.save()
        
        # tie with original
        original = LocationReference.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()        
            
        return clone               

'''
 OBJECTS TABLE, this describes basic building blocks for sources and destination
 parts of firewall rules, basic types are:
 - host, means a single X.X.X.X IP
 - range, means an X.X.X.X-Y.Y.Y.Y IP
 - subnet, means an X.X.X.X/Z subnet definition
'''
class AtomicNetworkObject(VersionAndOwnerControl):
    # NAME
    name = models.CharField(max_length=50)
    # NAME
    description = models.CharField(max_length=1000, blank=True)
    # TYPE
    OBJECT_TYPES = (
        ('4S', 'IPv4 Subnet'),
        ('4H', 'IPv4 Host'),
        ('4R', 'IPv4-to-IPv4 Range'),
    )    
    type = models.CharField(max_length=2, choices=OBJECT_TYPES)
    # IP1 part
    octet1 = models.PositiveSmallIntegerField()
    octet2 = models.PositiveSmallIntegerField()
    octet3 = models.PositiveSmallIntegerField()
    octet4 = models.PositiveSmallIntegerField()
    # Mask part
    mask = models.PositiveSmallIntegerField(null=True, blank=True, default=32)
    # IP2 part for RANGES
    range_octet1 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    range_octet2 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    range_octet3 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    range_octet4 = models.PositiveSmallIntegerField(null=True, blank=True, default=0)    
    # TO STRING
    def __str__(self):
        if self.type == '4S':
            return self.owner.prefix + "_" + self.name + " ( " + self.type + " : " + str(self.octet1) + "." + str(self.octet2) + "."+ str(self.octet3) + "."+ str(self.octet4) + "/" + str(self.mask) + "." +  " )"
        if self.type == '4H':
            return self.owner.prefix + "_" + self.name + " ( " + self.type + " : " + str(self.octet1) + "." + str(self.octet2) + "."+ str(self.octet3) + "."+ str(self.octet4) +  " )"
        if self.type == '4R':
            return self.owner.prefix + "_" + self.name + " ( " + self.type + " : " + str(self.octet1) + "." + str(self.octet2) + "."+ str(self.octet3) + "."+ str(self.octet4) + " - " + str(self.range_octet1) + "." + str(self.range_octet2) + "."+ str(self.range_octet3) + "."+ str(self.range_octet4) + "." +  " )"


    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning AtomicNetworkObject ID: " + str(objectid))                   
        # creating clone
        clone = AtomicNetworkObject.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;       
        # NEW RULE PRACTICALLY
        clone.save()
        
        # tie with original
        original = AtomicNetworkObject.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()
            
        return clone      


class StaticNetworkObjectGroup(VersionAndOwnerControl):
    # Name
    name = models.CharField(max_length=200)
    # Owner
    network_objects = models.ManyToManyField(AtomicNetworkObject)
    # TO STRING
    def __str__(self):
        included = "["
        for atomic_network_object in self.network_objects.all():
            included = included + str(atomic_network_object.owner.prefix  + "_" + atomic_network_object.name) + ";"
        included = included + "]"    
        return self.owner.prefix + "_" + str(self.name) + ": " + included   
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning StaticNetworkObjectGroup ID: " + str(objectid))                   
        # creating clone
        clone = StaticNetworkObjectGroup.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;       
        # NEW RULE PRACTICALLY
        clone.save()
        
        # tie with original
        original = StaticNetworkObjectGroup.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()     
                
        ''' 
        On this point the self became useless because we lost track of it 
        during initial cloning, we need to search again original rule by id
        '''
        
        # STATIC_SOURCE  
        for network_object in original.network_objects.all():
            successor_pk = int(network_object.successor.pk)
            Logger.debug("original port PK:" + str(network_object) + " but we are adding successor:" + str(successor_pk)) 
            clone.network_objects.add(AtomicNetworkObject.objects.filter(pk=successor_pk).get())
            
        return clone            
                       
 
 
  
class AtomicNetworkObjectToLocationBind(VersionAndOwnerControl): 
    # location
    location = models.ForeignKey(LocationReference, on_delete=models.CASCADE)
    # Owner
    network_objects = models.ManyToManyField(AtomicNetworkObject) 
    # STRING
    def __str__(self):
        return self.owner.prefix + "_" + str(self.location) + " -to- " + str(self.network_objects)
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning AtomicNetworkObjectToLocationBind ID: " + str(objectid))                   
        # creating clone
        clone = AtomicNetworkObjectToLocationBind.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.ownercontrol_ptr_id = None
        clone.version = clone.version + 1;        
        # NEW RULE PRACTICALLY
        clone.save()
        ''' 
        On this point the self became useless because we lost track of it 
        during initial cloning, we need to search again original rule by id
        '''
        # tie with original
        original = AtomicNetworkObjectToLocationBind.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()     
                
        # STATIC_SOURCE 
        if original.location is not None: 
            successor_pk = int(original.location.successor.pk)
            Logger.debug("original port PK:" + str(original.location) + " but we are adding successor:" + str(successor_pk)) 
            clone.location = LocationReference.objects.filter(pk=successor_pk).get() 
            clone.save()
            
        # STATIC_SOURCE  
        for network_object in original.network_objects.all():
            successor_pk = int(network_object.successor.pk)
            Logger.debug("original port PK:" + str(network_object) + " but we are adding successor:" + str(successor_pk)) 
            clone.network_objects.add(AtomicNetworkObject.objects.filter(pk=successor_pk).get())                      
            
        return clone     
    
    
    
class SystemMap(VersionAndOwnerControl):
    # Name
    name = models.CharField(max_length=200) 
    # DESCRIPTION
    description = models.CharField(max_length=1000, blank=True)  
    # LIST OF NW OBJECTS MAPPED TO THEIR LOCATIONS
    network_object_to_location_list = models.ManyToManyField(AtomicNetworkObjectToLocationBind)         
    # FUNCTION TO STR
    def __str__(self):
        included = "[ TODO "
        #for atomic_network_object in self.network_objects.all():
        #    included = included + str(atomic_network_object.owner.prefix  + "_" + atomic_network_object.name) + ";"
        included = included + "]"    
        return self.owner.prefix + "_" + str(self.name) + ": " + included 
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning SystemMap ID: " + str(objectid))                   
        # creating clone
        clone = SystemMap.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;        
        # NEW RULE PRACTICALLY
        clone.save()
        ''' 
        On this point the self became useless because we lost track of it 
        during initial cloning, we need to search again original rule by id
        '''
        original = SystemMap.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()     
                
        # STATIC_SOURCE  
        for network_object_to_location_list in original.network_object_to_location_list.all():
            successor_pk = int(network_object_to_location_list.successor.pk)
            Logger.debug("original port PK:" + str(network_object_to_location_list) + " but we are adding successor:" + str(successor_pk)) 
            clone.network_object_to_location_list.add(AtomicNetworkObjectToLocationBind.objects.filter(pk=successor_pk).get())                    
            
        return clone         
    


            
    
'''
    Ports are simple objects like "UDP" 9 or TCP 8080 that will be mapped
    to Services model to create services collections
'''
class Port(VersionAndOwnerControl):
    # Protocol
    PROTOCOL_TYPES = (
        ('U', 'UDP'),
        ('T', 'TCP'),
        ('I', 'ICMP'),
        ('*', 'ANY')
    )    
    protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPES) 
    # RANGE
    range = models.BooleanField(default=False);
    # DESCRIPTION
    description = models.CharField(max_length=1000,blank=True,null=True)
    # protocol number
    # NOTE: -1 means ANY
    number = models.IntegerField(default=-1)
    number2 = models.IntegerField(default=-1,blank=True)    
    # TO STRING
    def __str__(self):
        if self.range:
            return self.owner.prefix + "_" + str(self.protocol) + ":" + str(self.number) + "-" + str(self.number2)
        else:    
            return self.owner.prefix + "_" + str(self.protocol) + ":" + str(self.number)
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning Port ID: " + str(objectid))                   
        # creating clone
        clone = Port.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;        
        # NEW RULE PRACTICALLY
        clone.save()
        
        # tie with original
        original = Port.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()                

        return clone   
                        

'''
    NAME holder for service, like "http", which will then be referenced
    as Services that hold Ports object below
'''
class Service(VersionAndOwnerControl):
    # NAME
    name = models.CharField(max_length=200,default='') 
    def __str__(self):
        return self.owner.prefix + "_" + self.name 
    
    ports = models.ManyToManyField(Port)    
    
    @staticmethod
    def clone(objectid): 
        Logger.debug("Cloning Service ID: " + str(objectid))                   
        # creating clone
        clone = Service.objects.filter(pk=objectid).get()       
        clone.id = None
        clone.pk = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;      
        # NEW RULE PRACTICALLY
        clone.save()
        
        # tie with original
        original = Service.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()          
        ''' 
        On this point the self became useless because we lost track of it 
        during initial cloning, we need to search again original rule by id
        '''
        original = Service.objects.filter(pk=objectid).get() 
        
        # STATIC_SOURCE  
        for port in original.ports.all():
            successor_pk = int(port.successor.pk)
            Logger.debug("original port PK:" + str(port) + " but we are adding successor:" + str(successor_pk)) 
            clone.ports.add(Port.objects.filter(pk=successor_pk).get())
            
        return clone         
        


'''
    RULE TABLE, this describes basic firewall rules we are creating here
    Each rule has to has have source/destination (including ports via services) 
    and then action and owner group
'''
class Rule(ApprovalAndVersionAndOwnerControl):
    # Protocol
    ACTIONS = (
        ('P', 'PERMIT'),
        ('D', 'DENY')
    ) 
    action = models.CharField(max_length=1, choices=ACTIONS, default='P')         
    # STATICS
    static_source = models.ManyToManyField(StaticNetworkObjectGroup, related_name='static_source_network_objects', blank=True)
    static_destination = models.ManyToManyField(StaticNetworkObjectGroup, related_name='static_destination_network_objects', blank=True)
    # DYNAMICS
    DYNAMIC_TYPES = (
        ('S', 'SEMI-STATIC'),
        ('D', 'DYNAMIC'),
        ('A', 'ALL FORCED'),
    ) 
    dynamic_source_type = models.CharField(max_length=1, choices=DYNAMIC_TYPES, default='D') 
    dynamic_source_location = models.ForeignKey(LocationReference, on_delete=models.CASCADE,related_name='dynamic_source_location', blank=True, null=True)     
    dynamic_source = models.ManyToManyField(SystemMap, related_name='dynamic_source_network_objects', blank=True)
    dynamic_destination_type = models.CharField(max_length=1, choices=DYNAMIC_TYPES, default='D')    
    dynamic_destination_location = models.ForeignKey(LocationReference, on_delete=models.CASCADE,related_name='dynamic_destination_location', blank=True, null=True)
    dynamic_destination = models.ManyToManyField(SystemMap, related_name='dynamic_destination_network_objects', blank=True)
    # SOURCE SERVICE PORTS
    source_port_services = models.ManyToManyField(Service, related_name='source_port_services', blank=True)
    # DESTINATION SERVICE PORTS
    destination_port_services = models.ManyToManyField(Service, related_name='destination_port_services', blank=True) 
    # COMMENT
    comment = models.CharField(max_length=1000,null=True, blank=True,default='') 
    
    '''
    def __str__(self):
        sources_string = "SSRC:["
        for source_object in self.static_source.all():
            sources_string = sources_string + str(source_object) + ";"
        sources_string = sources_string + "]"
        
        destination_string = "SDST["
        for destination_object in self.dynamic_source.all():
            destination_string = destination_string + str(destination_object) + ";"
        destination_string = destination_string + "]"     
        
        sources_service_string = "S_SERVICE["
        for source_service_object in self.source_port_services.all():
            sources_service_string = sources_service_string + str(source_service_object) + ";"
        sources_service_string = sources_service_string + "]"
        
        destination_service_string = "D_SERVICE["
        for destination_service_object in self.destination_port_services.all():
            destination_service_string = destination_service_string + str(destination_service_object) + ";"
        destination_service_string = destination_service_string + "]"             
            
            
        return self.owner.prefix + "_[" + self.action + " " + sources_string +" " + sources_service_string +" " + destination_string + " " + destination_service_string + "] " + self.comment
    '''
    
    
    @staticmethod
    def clone(objectid):
        
        #import pdb; pdb.set_trace()
        
        Logger.debug("Cloning rule ID: " + str(objectid))                   
        
        clone = Rule.objects.filter(pk=objectid).get()  
        Logger.debug("Owned by: " + str(clone.owner))   
        
        # Clean the whole inheritance structure
        clone.id = None
        clone.pk = None
        clone.approvalandversionandownercontrol_ptr_id = None
        clone.versionandownercontrol_ptr_id = None
        clone.ownercontrol_ptr_id = None  
        clone.version = clone.version + 1;      
        
        # NEW RULE PRACTICALLY
        clone.save()
        Logger.debug("New owned by: " + str(clone.owner))

        ''' 
        On this point the self became useless because we lost track of it 
        during initial cloning, we need to search again original rule by id
        '''
        original = Rule.objects.filter(pk=objectid).get()
        original.successor = clone
        original.save()
        
        clone.predecessor = original
        clone.save()      
        
        '''
        Clone owner
        '''
        
        #import pdb; pdb.set_trace() 
        
        ''' 
        Foreign Key and Many to Many fields cloning is EXPLICIT
        '''
          
        # STATIC_SOURCE  
        for static_source in original.static_source.all():
            successor_pk = int(static_source.successor.pk)
            Logger.debug("original static_source PK:" + str(static_source) + " but we are adding successor:" + str(successor_pk)) 
            clone.static_source.add(StaticNetworkObjectGroup.objects.filter(pk=successor_pk).get())            
            
        # STATIC DESTINATION  
        for static_destination in original.static_destination.all():
            successor_pk = int(static_destination.successor.pk)
            Logger.debug("original static_destination PK:" + str(static_destination) + " but we are adding successor:" + str(successor_pk)) 
            clone.static_destination.add(StaticNetworkObjectGroup.objects.filter(pk=successor_pk).get())                         
            
        #dynamic_source_location
        if original.dynamic_source_location is not None: 
            successor_pk = int(original.dynamic_source_location.successor.pk)
            Logger.debug("original port PK:" + str(original.dynamic_source_location) + " but we are adding successor:" + str(successor_pk)) 
            clone.dynamic_source_location = LocationReference.objects.filter(pk=successor_pk).get() 
            clone.save()            
            
        #dynamic_destination_location
        if original.dynamic_destination_location is not None: 
            successor_pk = int(original.dynamic_destination_location.successor.pk)
            Logger.debug("original port PK:" + str(original.dynamic_destination_location) + " but we are adding successor:" + str(successor_pk)) 
            clone.dynamic_destination_location = LocationReference.objects.filter(pk=successor_pk).get() 
            clone.save()                    
        
        # DYNAMIC SOURCE  
        for dynamic_source in original.dynamic_source.all():
            successor_pk = int(dynamic_source.successor.pk)
            Logger.debug("original dynamic_source PK:" + str(dynamic_source) + " but we are adding successor:" + str(successor_pk)) 
            clone.dynamic_source.add(SystemMap.objects.filter(pk=successor_pk).get())              
            
        # DYNAMIC DESTINATION  
        for dynamic_destination in original.dynamic_destination.all():
            successor_pk = int(dynamic_destination.successor.pk)
            Logger.debug("original dynamic_destination PK:" + str(dynamic_destination) + " but we are adding successor:" + str(successor_pk)) 
            clone.dynamic_destination.add(SystemMap.objects.filter(pk=successor_pk).get())             
            
        # source_port_services
        for source_port_services in original.source_port_services.all():
            successor_pk = int(source_port_services.successor.pk)
            Logger.debug("original source_port_services PK:" + str(source_port_services) + " but we are adding successor:" + str(successor_pk)) 
            clone.source_port_services.add(Service.objects.filter(pk=successor_pk).get())              
            
        # destination_port_services 
        for destination_port_services in original.destination_port_services.all():
            successor_pk = int(destination_port_services.successor.pk)
            Logger.debug("original destination_port_services PK:" + str(destination_port_services) + " but we are adding successor:" + str(successor_pk)) 
            clone.destination_port_services.add(Service.objects.filter(pk=successor_pk).get())                                    
            
        return clone
        
     
        
 
        #for static_source in self.static_source.all():
        #    print('self static_source: ' + str(static_source))              
        
         
        
              
    
