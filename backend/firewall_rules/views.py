from django.shortcuts import render
from django.http import HttpResponse
from firewall_rules.views_classes.NetworkObjects import *
from firewall_rules.models import *
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from initialization.initialization import initialization
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib import messages;
from time import gmtime, strftime
import copy
import pprint

DEBUG = True

def get_version_control_context(request,**kwargs):
    context = {}
    if DEBUG:
        messages.add_message(request, messages.INFO, "DEBUG MODE IS ENABLED IN VIEWs")
    
    versionState = CurrentVersionState.getlatest()
    context.update({
                'versionState' : versionState
            })    
        
    return context 

def index(request, *args, **kwargs):    
    print("CONDITIONAL INITIALIZATON")
    initialization() 
    ''' 
    Information about user's groups
    '''
    groupextension_list = GroupExtension.getGroupExtensionForUser(request.user)
    context = {
            'groupextension_list' : groupextension_list,
        }
    template = loader.get_template('firewall_rules/index.html')
    context.update(get_version_control_context(request,**kwargs))
    return HttpResponse(template.render(context, request))

def about(request):
    print("CONDITIONAL INITIALIZATON")
    initialization() 
    context = {
            'about'     : 'about',
            'version'   : '0.001 alpha',
            'author'    : 'phavrila@gmail.com',              
        }
    template = loader.get_template('firewall_rules/index.html')
    context.update(get_version_control_context(request))
    
    return HttpResponse(template.render(context, request))

@login_required
def request_access(request):
    print("CONDITIONAL INITIALIZATON")
    initialization() 
    context = {
            'version'   : '0.001 alpha',
            'author'    : 'phavrila@gmail.com',              
        }
    template = loader.get_template('firewall_rules/index.html')
    return HttpResponse(template.render(context, request))

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect(reverse('firewall_rules_namespace:index'))

@login_required
def firewall_configuration(request):

    locations_for_fw_config_list = LocationReference.objects.all()      
    context = {
        'locations_for_fw_config_list': locations_for_fw_config_list,
    }
    
    context.update(get_version_control_context(request))

    template = loader.get_template('firewall_rules/index.html')
    return HttpResponse(template.render(context, request))

'''
 #################
 LIST VIES GENERIC
 #################
'''
class FirebrickListView(TemplateView):
    template_name = "firewall_rules/index.html"
    model = Rule
    context_object_name = 'rules_list'
    extra_context={'extra':'yes2'}
    
    def get_queryset(self):
        return list(set(Rule.getUseAllowedObjects(self.request.user) + Rule.getPromiscuousObjects()))     
    # 
    def get(self, request, *args, **kwargs):
        context={}
        objects_list = self.get_queryset()
        context.update({
            self.context_object_name : objects_list
        })
        
        # EXTRA CONTEXTS NEEDED
        context.update(self.extra_context)
        context.update(get_version_control_context(request,**kwargs))                
          
        # CONSTRUCT TEMPLATE WITH CONTEXT AND RETURN     
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))         
        

class CustomizedListView(generic.ListView):
    extra_context = {'extra':'yes!'}
    # OVERRIDE TO PROVIDE 'extra_context' capabilities
    def get_context_data(self, **kwargs):
        #context = super(self.__class__, self).get_context_data(**kwargs)
        context = super(generic.ListView,self).get_context_data(**kwargs)
        for key, value in self.extra_context.items():
            if callable(value):
                context[key] = value()
            else:
                context[key] = value
        return context    

class RulesView(FirebrickListView):
    context_object_name = 'rules_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(Rule.getUseAllowedObjects(self.request.user) + Rule.getPromiscuousObjects()))

class ServicesView(FirebrickListView):
    context_object_name = 'services_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(Service.getUseAllowedObjects(self.request.user) + Service.getPromiscuousObjects())) 

class PortsView(FirebrickListView):
    context_object_name = 'ports_list'
    template_name = 'firewall_rules/index.html'
    extra_context={'extra':'yes!'}
    #paginate_by = 2
    def get_queryset(self):
        return list(set(Port.getUseAllowedObjects(self.request.user) + Port.getPromiscuousObjects()))
    
class LocationsView(FirebrickListView):
    context_object_name = 'locations_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(LocationReference.getUseAllowedObjects(self.request.user) + LocationReference.getPromiscuousObjects()))

class AtomicNetworkObjectView(FirebrickListView):
    context_object_name = 'atomicnetworkobject_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(AtomicNetworkObject.getUseAllowedObjects(self.request.user) + AtomicNetworkObject.getPromiscuousObjects()))
    
class StaticNetworkObjectGroupView(FirebrickListView):
    context_object_name = 'staticnetworkobjectgroup_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(StaticNetworkObjectGroup.getUseAllowedObjects(self.request.user) + StaticNetworkObjectGroup.getPromiscuousObjects()))

class SystemMapView(FirebrickListView):
    context_object_name = 'systemmap_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(SystemMap.getUseAllowedObjects(self.request.user) + SystemMap.getPromiscuousObjects()))
    
class AtomicNetworkObjectToLocationBindView(FirebrickListView):
    context_object_name = 'atomicnetworkobjecttolocationbind_list'
    template_name = 'firewall_rules/index.html'
    def get_queryset(self):
        return list(set(AtomicNetworkObjectToLocationBind.getUseAllowedObjects(self.request.user) + AtomicNetworkObjectToLocationBind.getPromiscuousObjects()))

'''
 ######################
 DETAILED VIEWS GENERIC
 ######################
'''

class VersionControlView(TemplateView):
    template_name = "firewall_rules/index.html"
    extra_context={'version_control':'version_control view entered'}
    
    
    def get(self, request, *args, **kwargs):
        context={}
        template = loader.get_template(self.template_name)
        
        ''' CHECK INPUT '''
        if 'confirmed' in kwargs:
            command_context={'confirmed':"True"}
            context.update(command_context)
                    
        if 'command' not in kwargs:
            messages.add_message(request, messages.ERROR, "Missing version control COMMAND")
            return HttpResponse(template.render(context, request))

        messages.add_message(request, messages.INFO, "COMMAND: " + kwargs['command'])
        Logger.debug("COMMAND: " + str(kwargs['command']))
        command_context={'command':str(kwargs['command'])}
        context.update(command_context)
        
        '''
        COMMANDS PROCESSING START
        '''
        if str(kwargs['command']) == 'edit':
            if CurrentVersionState.getlatest().version_states != CurrentVersionState.APPROVED:
                messages.add_message(request, messages.ERROR, "You are trying to start DB clone and editing unlock from a wrong initial state!")
                return HttpResponse(template.render(context, request))
            elif not GroupExtension.bUserInAdminGroup(request.user):
                messages.add_message(request, messages.ERROR, "You are not allowed to change DB states!")
                return HttpResponse(template.render(context, request))                             
            else:
                '''
                CloneDB & increase version on success
                '''        
                if CurrentVersionState.cloneDB() == 0:
                    Logger.debug("DB Cloning successfull")
                    CurrentVersionState.increase(request.user)
                    CurrentVersionState.addcomment("New version at " + strftime("%a %b %d %H:%M:%S %Y", gmtime()), request.user)
                    
        elif str(kwargs['command']) == 'submit':
            if CurrentVersionState.getlatest().version_states != CurrentVersionState.EDITING:
                messages.add_message(request, messages.ERROR, "DB is not in state for review submission!")
                context.update(get_version_control_context(request,**kwargs))  
                return HttpResponse(template.render(context, request))
            elif not GroupExtension.bUserInAdminGroup(request.user):
                messages.add_message(request, messages.ERROR, "You are not allowed to change DB states!")
                return HttpResponse(template.render(context, request))              
            else:                   
                CurrentVersionState.addcomment("Submit at " + strftime("%a %b %d %H:%M:%S %Y", gmtime()), request.user)
                CurrentVersionState.edittimestamp()
                version_control = CurrentVersionState.getlatest()
                version_control.version_states = CurrentVersionState.REVIEW;
                version_control.save()
                context.update(get_version_control_context(request,**kwargs))  
                return HttpResponse(template.render(context, request))   

        elif str(kwargs['command']) == 'withdraw':
            if CurrentVersionState.getlatest().version_states != CurrentVersionState.REVIEW:
                messages.add_message(request, messages.ERROR, "DB is not in state for withdraw!")
                context.update(get_version_control_context(request,**kwargs))  
                return HttpResponse(template.render(context, request))
            elif not GroupExtension.bUserInAdminGroup(request.user):
                messages.add_message(request, messages.ERROR, "You are not allowed to change DB states!")
                return HttpResponse(template.render(context, request))              
            else:                   
                CurrentVersionState.addcomment("Withdrawal at " + strftime("%a %b %d %H:%M:%S %Y", gmtime()), request.user)
                version_control = CurrentVersionState.getlatest()
                version_control.version_states = CurrentVersionState.EDITING;
                version_control.save()
                context.update(get_version_control_context(request,**kwargs))  
                return HttpResponse(template.render(context, request))              
                                  
        else:
            messages.add_message(request, messages.ERROR, "UNKNOW COMMAND!")
            context.update(get_version_control_context(request,**kwargs))  
            return HttpResponse(template.render(context, request))             
                               
                
        '''
        Update context for view rendering
        '''
        context.update(self.extra_context)
        context.update(get_version_control_context(request,**kwargs))        
        return HttpResponse(template.render(context, request))          

'''
 ######################
 DETAILED VIEWS GENERIC
 ######################
'''

class FirebrickDetailView(TemplateView):
    template_name = "firewall_rules/index.html"
    model = Service
    context_object_name = 'service'
    after_edit_redirect_url_name = 'firewall_rules_namespace:services'
    model_field_names = [ 'name', 'owner_id']
    many_to_many_field_names = [ 'ports' ]
    foreign_key_field_names = []
    extra_context={'extra':'yes2'}
    
    # 
    def get(self, request, *args, **kwargs):
        if kwargs['command'] == 'delete':
            object = self.model.objects.get(pk=kwargs['pk'])
            Logger.log("User " + request.user.username + " deleted: " + str(object))
            object.delete()
            return redirect(reverse(self.after_edit_redirect_url_name))        
        
        if kwargs['command'] == 'new':
            object = self.model()
        else:
            object = self.model.objects.get(pk=kwargs['pk'])            
        
        group_extension_list = GroupExtension.getGroupExtensionForUser(request.user)   
        context = {
            self.context_object_name: object,
            
        } 
        context.update({
            'group_extension_list': group_extension_list,    
        })
        
        for many_to_many_field in self.many_to_many_field_names:
            # GET ALL OBJECTS OF THE TYPE
            m2m_class = object._meta.get_field(many_to_many_field).related_model
            m2m_values = list(set(m2m_class.getUseAllowedObjects(request.user) + m2m_class.getPromiscuousObjects()))
            for m2m_value in m2m_values:
                Logger.debug('m2m_values;' + str(m2m_value))
            context.update(
                {(many_to_many_field + "_m2mfield") : m2m_values}
            )
            # GET ALL THE OBJECTS OF ASSIGNED
            if kwargs['command'] != 'new':
                m2m_manager = getattr(object,many_to_many_field)
                m2m_selected_values = m2m_manager.all()
                for m2m_selected_value in m2m_selected_values:
                    Logger.debug('m2m_selected_value;' + str(m2m_selected_value))
                context.update(
                    {(many_to_many_field + "_m2mfield_selected") : m2m_selected_values}
                )
                
        for foreign_key_field in self.foreign_key_field_names:
            fk_class = object._meta.get_field(foreign_key_field).related_model
            fk_values = list(set(fk_class.getUseAllowedObjects(request.user) + fk_class.getPromiscuousObjects()))
            Logger.debug('fk_values;' + str(fk_values))
            context.update(
                {(foreign_key_field + "_fkfield") : fk_values}
            )     
            
            # GET ALL THE OBJECTS OF ASSIGNED
            if kwargs['command'] != 'new':
                fk_manager = getattr(object,foreign_key_field)
                fk_selected_value = fk_manager
                Logger.debug('fkfield_selected;' + str(fk_selected_value))
                context.update(
                    {(foreign_key_field + "_fkfield_selected") : fk_selected_value}
                )                   
            
        context.update(self.extra_context)                
        context.update(get_version_control_context(request,**kwargs))        
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))  
    
    def check_submitted_fields(self,request,model_field_values,many_to_many_field_values,foreign_keys_field_values):
        to_return = True;
        for field_name in self.model_field_names:
            if field_name not in request.POST:
                messages.add_message(request, messages.ERROR, 'Missing mandatory field' + field_name)
                to_return = False;                
        for field_name in self.many_to_many_field_names:
            if request.POST.getlist(field_name) is None or len(request.POST.getlist(field_name)) == 0:
                messages.add_message(request, messages.ERROR, 'Missing mandatory field' + field_name)
                to_return = False;                     
        for field_name in self.foreign_key_field_names:
            if field_name not in request.POST:
                messages.add_message(request, messages.ERROR, 'Missing mandatory field' + field_name)
                to_return = False;          
        
        return to_return
        
    
    def post(self, request, *args, **kwargs):
        if request.POST:
            model_field_values = []
            many_to_many_field_values = {} 
            foreign_keys_field_values = []          
            try:
                for field_name in self.model_field_names:
                    if request.POST[field_name] is None or request.POST[field_name] == '':
                        Logger.debug("ERROR: Empty mandatory field " + field_name)
                        model_field_values.append(None) 
                    else:
                        Logger.debug("POST extraction field_name: " + field_name + " resulted in " + request.POST[field_name])
                        model_field_values.append(request.POST[field_name])                        
                for field_name in self.many_to_many_field_names:
                    if request.POST.getlist(field_name) is None or len(request.POST.getlist(field_name)) == 0:
                        Logger.debug("ERROR: Empty mandatory m2m field " + field_name)
                        model_field_values.append(None)                      
                    for value_iteration in request.POST.getlist(field_name):
                        Logger.debug("POST extraction m2m_field_name: " + field_name + " resulted in " + value_iteration)
                    many_to_many_field_values.update(
                        { field_name : request.POST.getlist(field_name) } 
                    )
                for field_name in self.foreign_key_field_names:
                    if request.POST[field_name] is None or request.POST[field_name] == '':
                        Logger.debug("ERROR: Empty mandatory field " + field_name)
                        model_field_values.append(None)
                    else:
                        Logger.debug("POST extraction fk_field_name: " + field_name + " resulted in " + request.POST[field_name])
                        foreign_keys_field_values.append(request.POST[field_name])                       
                    
            except:
                return HttpResponse("YOUR POST DATA APPEARED TO BE INCORRECT")
            else:
                '''
                VALIDATE INPUT
                '''
                if not self.check_submitted_fields(request,model_field_values,many_to_many_field_values,foreign_keys_field_values):
                    messages.add_message(request, messages.ERROR, 'BAD POST PARAMETERS.')
                    #return redirect(reverse(request.resolver_match.url_name,request.resolver_match.args,request.resolver_match.kwargs))
                    return redirect(request.path)
                
                Logger.debug("COMMAND:" + kwargs['command'])
                if kwargs['command'] == 'edit':
                    try:
                        pk = kwargs['pk']
                        Logger.debug("PK from POST: " + str(pk))
                        model_instance = self.model.objects.get(pk=pk)
                    except:
                        return HttpResponse("THE EDITED ITEM WAS NO LONGER FOUND!")
                    else:
                        ''' 
                        CHANGE APPROVED STATE OF ONLY APPROVABLE OBJECT TO FALSE ON EDITING
                        '''
                        #if type(model_instance) is ApprovalAndVersionAndOwnerControl:
                        if isinstance(model_instance, ApprovalAndVersionAndOwnerControl):
                            Logger.debug("FirebrickDetailView - POST: detected instance of approvable object, setting to FALSE")
                            model_instance.approved = False;                          
                        
                        '''
                        CHANGE FIELDS OF OBJECT
                        '''                        
                        for field_name,field_value in zip(self.model_field_names,model_field_values):
                            Logger.debug("setattr( " + str(model_instance) + "," + field_name +  "," + str(field_value) + ")")
                            setattr(model_instance, field_name, field_value)
                        for field_name,field_value in zip(self.foreign_key_field_names,foreign_keys_field_values):
                            Logger.debug("setattr( " + str(model_instance) + "," + field_name +  "," + str(field_value) + ")")
                            fk_class = model_instance._meta.get_field(field_name).related_model.objects.get(pk=field_value)
                            setattr(model_instance, field_name, fk_class)                            
                        # WE NEED TO SAVE BEFORE WE CAN ADD many2many objects
                        model_instance.save()
                        # THIS WILL TAKE CARE OF ADDING ALL M2M FIELD OBJECTS SELECTED 
                        for field_name in self.many_to_many_field_names:
                            model_instance_m2m_field = getattr(model_instance,field_name)
                            # WE NEED TO DELETE ALL OBJECTS TO ENTER ONLY THE NEW ONES
                            #for child_instance in model_instance_m2m_field.all():
                            model_instance_m2m_field.clear()
                            for child_instance in many_to_many_field_values[field_name]:
                                model_instance_m2m_field.add(child_instance) 
                            
                                                            
                if kwargs['command'] == 'new':                   
                    #try:
                    Logger.debug("ENTERING COMMAND NEW SECTION")
                    model_instance = self.model()
                    Logger.debug("Self model: " + str(model_instance))
                    for field_name,field_value in zip(self.model_field_names,model_field_values):
                        Logger.debug("setattr( " + str(model_instance) + "," + field_name +  "," + str(field_value) + ")")
                        setattr(model_instance, field_name, field_value)
                    for field_name,field_value in zip(self.foreign_key_field_names,foreign_keys_field_values):
                        Logger.debug("setattr( " + str(model_instance) + "," + field_name +  "," + str(field_value) + ")")
                        fk_class = model_instance._meta.get_field(field_name).related_model.objects.get(pk=field_value)
                        setattr(model_instance, field_name, fk_class)                             
                    # WE NEED TO SAVE BEFORE WE CAN ADD many2many objects
                    model_instance.save()
                    Logger.debug("new model saved")
                    # THIS WILL TAKE CARE OF ADDING ALL M2M FIELD OBJECTS SELECTED 
                    for field_name in self.many_to_many_field_names:
                        model_instance_m2m_field = getattr(model_instance,field_name)
                        for child_instance in many_to_many_field_values[field_name]:
                            model_instance_m2m_field.add(child_instance)                        
                    #except:
                    #    return HttpResponse("Failed to instantiate new object")
                return redirect(reverse(self.after_edit_redirect_url_name))
        return redirect(reverse(self.after_edit_redirect_url_name))          
    
class FirebrickServiceDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = Service
    context_object_name = 'service'
    after_edit_redirect_url_name = 'firewall_rules_namespace:services'
    model_field_names = [ 'name', 'owner_id']
    many_to_many_field_names = [ 'ports' ]
    
class FirebrickPortDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = Port
    context_object_name = 'port'
    after_edit_redirect_url_name = 'firewall_rules_namespace:ports'
    model_field_names = [ 'protocol', 'range','description','number','number2','owner_id']
    many_to_many_field_names = []  
    
class FirebrickLocationDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = LocationReference
    context_object_name = 'location'
    after_edit_redirect_url_name = 'firewall_rules_namespace:locations'
    model_field_names = [ 'name', 'description','prefix','owner_id']
    many_to_many_field_names = []  
    
class FirebrickAtomicNetworkObjectDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = AtomicNetworkObject
    context_object_name = 'atomicnetworkobject'
    after_edit_redirect_url_name = 'firewall_rules_namespace:atomicnetworkobjects'
    model_field_names = [ 'name', 'description','prefix','owner_id']
    many_to_many_field_names = [] 
    
class FirebrickStaticNetworkObjectGroupDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = StaticNetworkObjectGroup
    context_object_name = 'staticnetworkobjectgroup'
    after_edit_redirect_url_name = 'firewall_rules_namespace:staticnetworkobjectgroups'
    model_field_names = [ 'name','owner_id']
    many_to_many_field_names = ['network_objects'] 
    
class FirebrickSystemMapDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = SystemMap
    context_object_name = 'systemmap'
    after_edit_redirect_url_name = 'firewall_rules_namespace:systemmaps'
    model_field_names = [ 'name','owner_id','description']
    many_to_many_field_names = ['network_object_to_location_list'] 
    
  
class FirebrickAtomicNetworkObjectToLocationBindDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = AtomicNetworkObjectToLocationBind
    context_object_name = 'atomicnetworkobjecttolocationbind'
    after_edit_redirect_url_name = 'firewall_rules_namespace:atomicnetworkobjecttolocationbinds'
    model_field_names = [ 'owner_id']
    many_to_many_field_names = ['network_objects']   
    foreign_key_field_names = ['location']       
    
class FirebrickRuleDetailView(FirebrickDetailView):
    template_name = "firewall_rules/index.html"
    model = Rule
    context_object_name = 'rule'
    after_edit_redirect_url_name = 'firewall_rules_namespace:rules'
    model_field_names = [ 'owner_id','comment','action','dynamic_source_type','dynamic_destination_type']
    many_to_many_field_names = ['static_source','static_destination','dynamic_source','dynamic_destination','source_port_services','destination_port_services']   
    foreign_key_field_names = ['dynamic_source_location','dynamic_destination_location']       
    
    '''
    Custom parameter checks here
    '''
    def check_submitted_fields(self,request,model_field_values,many_to_many_field_values,foreign_keys_field_values):
        to_return = True;
        
        mandatory = [ 'owner_id','comment','action', 'source_port_services', 'destination_port_services' ] 
                  
        for field_name in mandatory:
            if field_name not in request.POST or request.POST[field_name] is None or request.POST[field_name] == '':
                messages.add_message(request, messages.ERROR, 'Missing mandatory field' + field_name)
                to_return = False;   
                
        ''' At least one source type needed '''
        if 'static_source' not in request.POST and 'dynamic_source' not in request.POST :
            messages.add_message(request, messages.ERROR, 'At least one static source or dynamic source is needed, Note that if you want "ANY", you need to explicitly add such static source')
            to_return = False; 
            
        ''' At least one destination type needed '''
        if 'static_destination' not in request.POST and 'dynamic_destination' not in request.POST :
            messages.add_message(request, messages.ERROR, 'At least one static destination or dynamic destination is needed, Note that if you want "ANY", you need to explicitly add such static destination')
            to_return = False;             
            
            
        return to_return         
    

    
    

