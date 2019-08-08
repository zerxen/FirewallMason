################
# FIREWALL MASON 
################
Small firewall rules management app for myself using Django framework to help our work team manage rules between multiple teams without relying on ticketing

#############################
# Python library dependencies
#############################
pip2 install django
pip2 install python-ldap
#pip2 install django-auth-ldap
#pip2 install djangorestframework
pip2 install markdown       # Markdown support for the browsable API.
pip2 install django-filter  # Filtering support
pip2 install django-cors-headers
pip2 install coreapi

#Mysql connector
apt-get install python-dev
pip2 install mysqlclient

#############################
# First run Django DB setup
#############################
1) Edit settings.py for your database connection, I am using MySQL here so update at least credentials for MySQL

Here is an example MySQL settings that will match the defaults from the git cloned:
CREATE DATABASE firewall_mason_db;
CREATE USER 'firewall_mason_user'@'localhost' IDENTIFIED BY 'devPassword123';
GRANT ALL ON firewall_mason_db.* TO 'firewall_mason_user'@'localhost';
FLUSH PRIVILEGES;

2) Prepare Django DB models with commands:
python manage.py makemigrations
python manage.py migrate
3) After first ever run go to <URL>/firewall_rules and the system will self-initialize with some basic data (users, few rules, etc..) to give you an easy to delete small example

