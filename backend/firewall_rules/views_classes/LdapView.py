import ldap
from django_auth_ldap.config import LDAPSearch
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
import logging

def ldap_auth(request):
    email = ""
    password = ""
    state = "empty"

    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("DEBUG: " + email + "/" +  password)
        
        logger = logging.getLogger('django_auth_ldap')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)        

        print("DEBUG(OPT_X_TLS_REQUIRE_CERT): " + str(ldap.get_option(ldap.OPT_X_TLS_REQUIRE_CERT)))
        print("DEBUG(OPT_X_TLS_NEVER): " + str(ldap.OPT_X_TLS_NEVER))
        
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            state = "Valid account"
        else:
            state = "Inactive account"
        
    ## NORMAL RENDER
    template = loader.get_template('firewall_rules/ldap_auth.html')
    #context = RequestContext(request, {'state': state, 'username': username})
    context = {
        'state': state, 
        'email': email
    }
    #return render_to_response('firewall_rules/ldap_auth.html', RequestContext(request, {'state': state, 'username': username}))  
    return HttpResponse(template.render(context, request))