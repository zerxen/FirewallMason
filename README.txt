################
# FIREWALL MASON 
################
Small firewall rules management app for myself using Django framework to help our work team manage rules between multiple teams without relying on ticketing

#############################
# Python library dependencies
#############################
pip2 install python-ldap
pip2 install django-auth-ldap
pip2 install djangorestframework
pip2 install markdown       # Markdown support for the browsable API.
pip2 install django-filter  # Filtering support
pip2 install django-cors-headers

#############################
# First run Django DB setup
#############################
1) Edit settings.py for your database connection, I am using MySQL here so update at least credentials for MySQL
2) Prepare Django DB models with commands:
python manage.py makemigrations
python manage.py migrate
3) After first ever run go to <URL>/firewall_rules and the system will self-initialize with some basic data (users, few rules, etc..) to give you an easy to delete small example

