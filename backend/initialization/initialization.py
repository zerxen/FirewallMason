# INITIALIZATION
#python2 manage.py shell

# IMPORT
from django.contrib.auth.models import Group, User
from firewall_rules.models import *
from Tkconstants import CURRENT

def initialization():
    
    initialized_log = Logger.objects.filter(log_text='INITIALIZED').first()
    if initialized_log is not None and initialized_log.log_text == 'INITIALIZED':
        return   
    
    print("Initialization started ...")
    Logger.log('INITIALIZED')

    
    #######################
    # SYSTEM group creation
    #######################
    ga = Group(name='system_admins')
    ga.save()
    gaex = GroupExtension(email='peter.havrila@hpe.com',description='All_GENERAL_OBJECTS_ARE_OWNED_BY_THIS_GROUP_DO_NOT_TOUCH', prefix='SYS',group=ga)
    gaex.promiscuous=True;
    gaex.admin=True;
    gaex.approvers=True;
    gaex.save()
    
    # local admin creation
    user=User.objects.create_user('admin', password='kreten123')
    user.is_superuser=True
    user.is_staff=True
    user.save()
    user.groups.add(ga)
    user.save()
    
    #######################
    # VERSIONING INIT
    #######################
    CurrentVersionState.increase(user) 
    current_version = CurrentVersionState.objects.filter(pk=1).get()
    current_version.version_states = CurrentVersionState.APPROVED
    current_version.save()  
    CurrentVersionState.edittimestamp()
    CurrentVersionState.approvetimestamp()
    
    ########################
    # Network group creation
    ########################
    g = Group(name='NextGenNetworkTeam')
    g.save()
    gex = GroupExtension(email='icc@hpe.com',description='Lazy, but smart', prefix='NGNW',promiscuous=False,group=g)
    gex.save()
    
    # test user creation
    user2=User.objects.create_user('peter.havrila@hpe.com', password='kreten123')
    user2.is_superuser=False
    user2.is_staff=False
    user2.save()
    user2.groups.add(g)
    user2.save()
    
    #######
    # PORTS
    #######
    port1 = Port(protocol='T',range=False,number=80,owner=gaex)
    port1.save()
    port2 = Port(protocol='T',range=False,number=8080,owner=gaex)
    port2.save()
    port3 = Port(protocol='T',range=False,number=443,owner=gaex)
    port3.save()
    port4 = Port(protocol='T',range=False,number=8443,owner=gaex)
    port4.save()
    port5 = Port(protocol='T',range=False,number=53,owner=gaex)
    port5.save()
    port6 = Port(protocol='U',range=False,number=53,owner=gaex)
    port6.save()
    port_ALL = Port(protocol='T',range=True,number=1,number2=65535, owner=gaex)
    port_ALL.save()
    
    #########
    # SERVICE
    #########
    s_http = Service(name='HTTP',owner=gaex)
    s_http.save()
    s_http.ports.add(*[port1,port2,port3,port4])
    s_dns = Service(name='DNS',owner=gaex)
    s_dns.save()
    s_dns.ports.add(*[port5,port6])
    s_all = Service(name='ALL',owner=gaex)
    s_all.save()
    s_all.ports.add(*[port_ALL])
    
    ###########
    # Locations
    ###########
    l1 = LocationReference(name='Alpharetta DC', prefix='ATC')
    l1.save()
    l2 = LocationReference(name='Suwanee DC', prefix='SWN') 
    l2.save()
    l3 = LocationReference(name='VPC Core', prefix='CORE1')
    l3.save() 
    
    ############################
    # Example atomic net objects
    ############################
    a1 = AtomicNetworkObject(name='ATC host',type='4H',octet1=1,octet2=1,octet3=1,octet4=1,owner=gaex)
    a1.save()
    a2 = AtomicNetworkObject(name='SWN host',type='4H',octet1=2,octet2=2,octet3=2,octet4=2,owner=gaex)
    a2.save()
    a3 = AtomicNetworkObject(name='CORE1 host',type='4H',octet1=10,octet2=10,octet3=10,octet4=10,owner=gaex)
    a3.save()
    a4 = AtomicNetworkObject(name='CORE1 host',type='4H',octet1=100,octet2=100,octet3=100,octet4=100,owner=gaex)
    a4.save()
    a5 = AtomicNetworkObject(name='google DNS1',type='4H',octet1=8,octet2=8,octet3=8,octet4=8,owner=gaex)
    a5.save()
    a6 = AtomicNetworkObject(name='google DNS2',type='4H',octet1=8,octet2=8,octet3=4,octet4=4,owner=gaex)
    a6.save()
    a7 = AtomicNetworkObject(name='DXC Net15',type='4S',octet1=15,octet2=0,octet3=0,octet4=0,mask=8,owner=gaex)
    a7.save()
    
    ############################
    # Atomics to Static Group
    ############################
    static1 = StaticNetworkObjectGroup(name='Google DNSs')
    static1.save()
    static1.network_objects.add(*[a5,a6])
    static2 = StaticNetworkObjectGroup(name='DXC Net15')
    static2.save()
    static2.network_objects.add(a7)
    
    ############################
    # Atomics to Locations
    ############################
    bind1 = AtomicNetworkObjectToLocationBind(location=l1,owner=gaex)
    bind1.save()
    bind1.network_objects.add(a1)
    bind2 = AtomicNetworkObjectToLocationBind(location=l2,owner=gaex)
    bind2.save()
    bind2.network_objects.add(a2)
    bind3 = AtomicNetworkObjectToLocationBind(location=l3,owner=gaex)
    bind3.save()
    bind3.network_objects.add(a3)
    bind4 = AtomicNetworkObjectToLocationBind(location=l3,owner=gaex)
    bind4.save()
    bind4.network_objects.add(a4)
    
    ############################
    # Multi-DC system1 map
    ############################
    system1 = SystemMap(name='MultiDC system1',description='example of DC with systems in different DCs')
    system1.save()
    system1.network_object_to_location_list.add(*[bind1,bind2,bind3,bind4])
    
    
    ############################
    # RULES - per type 
    ############################
    
    # Type0 - static,static
    r0 = Rule(comment='Type 0 rule',owner=gaex)
    r0.version = 1;
    r0.approved = True;
    r0.approved_by = user;
    r0.save()
    r0.static_source.add(static2)
    r0.static_destination.add(static1)
    r0.source_port_services.add(s_all)
    r0.destination_port_services.add(s_http)
    
    
    
    r1 = Rule(comment='Second Rule',owner=gaex)
    r1.version = 1;
    r1.approved = True;
    r1.approved_by = user;    
    r1.save()
    r1.static_source.add(static2)
    r1.dynamic_destination.add(system1)
    r1.source_port_services.add(s_all)
    r1.destination_port_services.add(s_dns)
    
    
    r2 = Rule(comment='Third Rule',owner=gaex)
    r2.version = 1;
    r2.approved = True;
    r2.approved_by = user;    
    r2.save()
    r2.dynamic_source.add(system1)
    r2.dynamic_destination.add(system1)
    r2.dynamic_destination_type = 'S';
    r2.dynamic_destination_location = l1
    r2.source_port_services.add(s_all)
    r2.destination_port_services.add(s_dns)
    r2.save()    
    
    
    
    
    
    










