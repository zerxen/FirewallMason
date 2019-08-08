from django.contrib import admin
from .models import *
# Register your models here.

# ADMIN CUSTOMIZATION
admin.site.site_header = "VPC NextGen Managemet Firewall Rules Central Repository";
admin.site.site_title = "VPC NextGen Managemet Firewall Rules Central Repository";
admin.site.index_title = "Repository Data Models";

class GroupAdmin(admin.ModelAdmin):
    fields = [ 'email', 'description','prefix','group']
    #filter_horizontal = ('members',)
admin.site.register(GroupExtension, GroupAdmin)

class PortsAdmin(admin.ModelAdmin):
    fields = ['approved','protocol','range', 'number','number2','owner','description']
admin.site.register(Port, PortsAdmin)
  
class ServicesAdmin(admin.ModelAdmin):    
    save_on_top = True
    fields = ['name', 'owner','ports']
    filter_horizontal = ('ports',)
    list_filter = ['owner']
    search_fields = ['name']    
admin.site.register(Service, ServicesAdmin)

class AtomicNetworkObjectAdmin(admin.ModelAdmin):
    fields = ['name', 'type', 'description','owner','octet1', 'octet2','octet3','octet4', 'mask','range_octet1','range_octet2', 'range_octet3','range_octet4'] 
admin.site.register(AtomicNetworkObject, AtomicNetworkObjectAdmin)

class NetworkObjectGroupAdmin(admin.ModelAdmin):
    fields = ['name','network_objects', 'owner']
    filter_horizontal = ('network_objects',)
admin.site.register(StaticNetworkObjectGroup, NetworkObjectGroupAdmin)

class SystemMapAdmin(admin.ModelAdmin):
    fields = ['name','description', 'network_object_to_location_list']
    filter_horizontal = ('network_object_to_location_list',)
admin.site.register(SystemMap, SystemMapAdmin)

class AtomicNetworkObjectToLocationBindAdmin(admin.ModelAdmin):
    fields = ['location','network_objects']
    filter_horizontal = ('network_objects',)
admin.site.register(AtomicNetworkObjectToLocationBind, AtomicNetworkObjectToLocationBindAdmin)

class RulesObjectsAdmin(admin.ModelAdmin):
    fields = ['version','rejected','edited_by','approved_by','approved','action', 'dynamic_source','static_source','source_port_services','static_destination','dynamic_destination','destination_port_services','comment','owner']
    #inlines = [RuleInline]
    filter_horizontal = ('static_source','source_port_services','static_destination','destination_port_services','dynamic_source','dynamic_destination')
admin.site.register(Rule, RulesObjectsAdmin)

class LocationReferenceAdmin(admin.ModelAdmin):
    fields = ['name','description', 'prefix']
admin.site.register(LocationReference, LocationReferenceAdmin)     

