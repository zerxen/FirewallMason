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
from doc.INSTALLS.initialization import initialization
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView




class RulesView(TemplateView):
    template_name = "firewall_rules/index.html"
    model = Rule
    context_object_name = 'rule'
    after_edit_redirect_url_name = 'firewall_rules_namespace:services'
    model_field_names = [ 'name', 'owner_id']
    many_to_many_field_names = [ 'ports' ]
    foreign_key_field_names = []
    
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
            
               
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))         
        